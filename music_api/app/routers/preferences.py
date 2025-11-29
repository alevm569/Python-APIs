from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.db import get_session
from app.models import PreferenceCreate, PreferenceRead
import app.crud as crud

router = APIRouter()


@router.post("/", response_model=PreferenceRead, status_code=status.HTTP_201_CREATED)
def add_preference(
    user_id: int,
    payload: PreferenceCreate,
    session: Session = Depends(get_session)
):
    """
    Añadir una preferencia musical a un usuario.
    """
    try:
        pref = crud.add_preference(session, user_id, payload)
        return pref
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[PreferenceRead])
def list_preferences(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Listar todas las preferencias de un usuario.
    """
    return crud.list_preferences(session, user_id)


@router.delete("/{pref_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preference(
    user_id: int,
    pref_id: int,
    session: Session = Depends(get_session)
):
    """
    Eliminar una preferencia por ID.
    """
    ok = crud.delete_preference(session, pref_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Preference not found")
    return None
