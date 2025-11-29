from typing import List, Optional
from sqlmodel import select, Session
from app.models import User, Preference, UserCreate, PreferenceCreate

# USERS
def create_user(session: Session, user_in: UserCreate) -> User:
    # verifica si existe email o username
    stmt = select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    exists = session.exec(stmt).first()
    if exists:
        raise ValueError("Usuario con ese email o username ya existe.")
    user = User.from_orm(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def list_users(session: Session, offset: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(offset).limit(limit)
    return session.exec(stmt).all()

def update_user(session: Session, user_id: int, data: dict) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    for k, v in data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    prefs = session.exec(select(Preference).where(Preference.user_id == user_id)).all()
    for p in prefs:
        session.delete(p)
    session.delete(user)
    session.commit()
    return True

# PREFERENCES
def add_preference(session: Session, user_id: int, pref_in: PreferenceCreate) -> Preference:
    user = session.get(User, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")
    
    pref = Preference(
        genre=pref_in.genre,
        favorite_artists=pref_in.favorite_artists,
        favorite_tracks=pref_in.favorite_tracks,
        user_id=user_id 
    )
    
    session.add(pref)
    session.commit()
    session.refresh(pref)
    return pref

def list_preferences(session: Session, user_id: int) -> List[Preference]:
    stmt = select(Preference).where(Preference.user_id == user_id)
    return session.exec(stmt).all()

def delete_preference(session: Session, pref_id: int) -> bool:
    pref = session.get(Preference, pref_id)
    if not pref:
        return False
    session.delete(pref)
    session.commit()
    return True
