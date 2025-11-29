from typing import Optional, List
from pydantic import Field
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects.mysql import JSON
from pydantic import EmailStr

# -----------------------
# MODELOS
# -----------------------
class PreferenceBase(SQLModel):
    genre: Optional[str] = None
    favorite_artists: Optional[List[str]] = Field(default_factory=list)
    favorite_tracks: Optional[List[str]] = Field(default_factory=list)

class Preference(PreferenceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    # definiciones JSON 
    favorite_artists: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)      
    )
    favorite_tracks: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)      
    )

    # Relación devuelta al usuario
    user: Optional["User"] = Relationship(back_populates="preferences")

# -----------------------
# MODELOS DE USUARIO
# -----------------------
class UserBase(SQLModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Un usuario puede tener muchas preferencias
    preferences: List[Preference] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class PreferenceCreate(PreferenceBase):
    pass

class PreferenceRead(PreferenceBase):
    id: int
    user_id: int
