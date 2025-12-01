from fastapi import FastAPI, Depends
from sqlmodel import Session
from sqlalchemy import text
from app.db import get_session, init_db
from app.routers import users, preferences
from app.routers import spotify

app = FastAPI()

# Rutas
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(preferences.router, prefix="/users/{user_id}/preferences", tags=["preferences"])
app.include_router(spotify.router, prefix="/spotify", tags=["spotify"])

@app.get("/")
def root():
    return {"message": "API funcionando correctamente!"}

@app.get("/check-db")
def check_db(session: Session = Depends(get_session)):
    try:
        session.exec(text("SELECT 1"))
        return {"status": "ok", "message": "Conexión a la base de datos exitosa"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.on_event("startup")
def on_startup():
    init_db()