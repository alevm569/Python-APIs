import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from app import models
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True  # verifica si la conexión está viva
)

def init_db():
    """
    Inicializa las tablas en la base de datos si no existen.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Provee una sesión de base de datos para FastAPI.
    """
    with Session(engine) as session:
        yield session
