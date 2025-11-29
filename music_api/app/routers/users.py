from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.db import get_session
from app.models import UserCreate, UserRead, UserUpdate
import app.crud as crud

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    try:
        user = crud.create_user(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return user

@router.get("/", response_model=List[UserRead])
def list_users(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return crud.list_users(session, offset=offset, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, session: Session = Depends(get_session)):
    updated = crud.update_user(session, user_id, payload.dict(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_user(session, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
