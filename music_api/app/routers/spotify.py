from fastapi import APIRouter, Depends, HTTPException, Query, requests
from sqlmodel import Session, select
from app.spotify_client import spotify_search, get_artist_top_tracks
from app.db import get_session
from app.models import Preference
import logging

router = APIRouter()
log = logging.getLogger(__name__)

@router.get("/search")
def search_spotify(
    q: str = Query(..., min_length=1),
    type: str = Query("track", regex="^(track|artist|album)$"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Endpoint para buscar canciones / artistas / albumes en Spotify.
    """
    return spotify_search(query=q, type=type, limit=limit)

@router.get("/users/{user_id}/spotify/favorites")
def spotify_favorites(user_id: int, session: Session = Depends(get_session)):
    """ 1. Toma el PRIMER artista favorito del usuario - busca sus canciones. 
        2. Toma la SEGUNDA canción favorita - busca su información. 
    """
    # Obtener preferencias del usuario
    stmt = select(Preference).where(Preference.user_id == user_id)
    pref = session.exec(stmt).first()

    if not pref:
        raise HTTPException(status_code=404, detail="El usuario no tiene preferencias guardadas.")

    # Validar artistas
    if not pref.favorite_artists or len(pref.favorite_artists) == 0:
        raise HTTPException(status_code=400, detail="No hay artistas favoritos para buscar.")

    artist_query = pref.favorite_artists[0]

    # Buscar artista
    try:
        artist_result = spotify_search(query=artist_query, type="artist", limit=1)
        artist_items = artist_result.get("artists", {}).get("items", [])
        if not artist_items:
            raise HTTPException(status_code=404, detail="No se encontró el artista en Spotify.")
        artist_id = artist_items[0].get("id")
        if not artist_id:
            raise HTTPException(status_code=404, detail="No se encontró el id del artista.")
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Error buscando artista en Spotify")
        raise HTTPException(status_code=502, detail="Error al comunicarse con Spotify para buscar el artista.")

    # Obtener top tracks usando funcion dedicada en el client
    try:
        top_tracks_resp = get_artist_top_tracks(artist_id, market="US")
    except requests.exceptions.RequestException as e:
        log.exception("Error obteniendo top tracks")
        raise HTTPException(status_code=502, detail="Error al obtener top tracks del artista en Spotify.")

    # Buscar la segunda cancion favorita
    if not pref.favorite_tracks or len(pref.favorite_tracks) < 2:
        raise HTTPException(status_code=400, detail="No hay suficientes canciones favoritas para buscar.")

    track_query = pref.favorite_tracks[1]
    try:
        track_result = spotify_search(query=track_query, type="track", limit=1)
    except Exception:
        log.exception("Error buscando track en Spotify")
        raise HTTPException(status_code=502, detail="Error al buscar la pista en Spotify.")

    return {
        "artist_searched": artist_query,
        "artist_top_tracks": top_tracks_resp,
        "track_searched": track_query,
        "track_info": track_result
    }