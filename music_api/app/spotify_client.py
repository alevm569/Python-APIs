import base64
import time
import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# credenciales spotify
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TOKEN_URL = "https://accounts.spotify.com/api/token"

# variables para cache del token
_token = None
_token_expires = 0


def get_token():
    """
    Obtiene token usando Client Credentials Flow y lo cachea.
    """
    global _token, _token_expires

    # Si el token actual sigue vigente, lo reutilizamos
    if _token and time.time() < _token_expires - 30:
        return _token

    # Caso contrario, pedimos uno nuevo
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error obteniendo token de Spotify")

    token_data = response.json()

    _token = token_data["access_token"]
    _token_expires = time.time() + token_data.get("expires_in", 3600)

    return _token


def spotify_search(query: str, type: str = "track", limit: int = 10):
    """
    Llama al endpoint de busqueda de Spotify.
    """
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": type,
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error llamando la API de Spotify")

    return response.json()

def get_artist_top_tracks(artist_id: str, market: str = "US", limit: int = 10) -> dict:
    token = get_token()
    resp = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        params={"market": market},
        headers={"Authorization": f"Bearer {token}"},
        timeout=5
    )
    resp.raise_for_status()
    return resp.json()