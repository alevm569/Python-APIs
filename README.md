# Python-APIs — FastAPI + MySQL + Spotify Web API

API RESTful desarrollada con **FastAPI**, **MySQL** y **Spotify Web API**.

Incluye funcionalidades para:

- Gestión de usuarios
- Registro y consulta de preferencias musicales
- Integración con Spotify (búsquedas, top tracks, detalles)
- Validación automática con Pydantic
- Documentación interactiva mediante Swagger (`/docs`)

## Estructura del Proyecto

```
music_api/
│── app/
│   ├── main.py               # Inicialización de la app + registro de rutas
│   ├── models.py             # Modelos SQLModel + validaciones Pydantic
│   ├── db.py                 # Conexión a MySQL + creación de tablas
│   ├── crud.py               # Lógica CRUD para usuarios y preferencias
│   ├── spotify_client.py     # Autenticación y peticiones a Spotify Web API
│   └── routers/
│       ├── users.py          # Endpoints CRUD de usuarios
│       ├── preferences.py    # Endpoints CRUD de preferencias
│       └── spotify.py        # Endpoints de integración con Spotify
│── requirements.txt
│── .env.example              # Variables de entorno requeridas
└── README.md
```

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Paquetes incluidos:

- fastapi
- uvicorn
- sqlmodel
- pymysql
- requests
- python-dotenv

## Configuración de Variables de Entorno

Crear un archivo `.env` siguiendo esta estructura:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=music_api_db

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

## Configuración de la Base de Datos MySQL

```sql
CREATE DATABASE music_api_db;

CREATE USER 'music_user'@'%' IDENTIFIED BY 'tu_password';

GRANT ALL PRIVILEGES ON music_api_db.* TO 'music_user'@'%';

FLUSH PRIVILEGES;
```

## Modelado de Datos

### Tabla: User

- id
- username
- email
- full_name
- relación 1–N con preferencias

### Tabla: Preference

- id
- user_id
- genre
- favorite_artists (JSON)
- favorite_tracks (JSON)

<img width="468" height="448" alt="image" src="https://github.com/user-attachments/assets/0f314772-3a20-4785-bbfc-8d90592fd29b" />

## Endpoints — Usuarios

### Crear usuario  
`POST /users/`

```json
{
  "username": "valery",
  "email": "valery@example.com",
  "full_name": "Valery Villarruel"
}
```
```python
def create_user(session: Session, user_in: UserCreate) -> User:
    stmt = select(User).where(
        (User.email == user_in.email) | (User.username == user_in.username)
    )
    exists = session.exec(stmt).first()
    if exists:
        raise ValueError("Usuario con ese email o username ya existe.")

    user = User.from_orm(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```
Descripción:

- Verifica si email o username ya existen.

- Crea el usuario validado por Pydantic (UserCreate).

- Guarda y retorna el objeto persistido.
  
### Listar usuarios  
`GET /users/`
```python
def list_users(session: Session, offset: int = 0, limit: int = 100):
    stmt = select(User).offset(offset).limit(limit)
    return session.exec(stmt).all()
```

### Obtener usuario por ID  
`GET /users/{id}`
```python
def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)
```

### Actualizar usuario  
`PUT /users/{id}`
```python
def update_user(session: Session, user_id: int, data: dict):
    user = session.get(User, user_id)
    if not user:
        return None
    for k, v in data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

### Eliminar usuario  
`DELETE /users/{id}`

## Preferencias Musicales

### Agregar preferencia  
`POST /users/{user_id}/preferences/`

```json
{
  "genre": "rock",
  "favorite_artists": ["Arctic Monkeys", "The Strokes"],
  "favorite_tracks": ["Do I Wanna Know", "505"]
}
```

```python
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
```

### Listar preferencias  
`GET /users/{user_id}/preferences/`

### Eliminar preferencia  
`DELETE /users/{user_id}/preferences/{pref_id}`

## Integración con Spotify Web API

La API implementa:

- Client Credentials Flow
- Cache interno del token
- Peticiones a `https://api.spotify.com/v1/search`

Toda la lógica está en:

```
app/spotify_client.py
```
Resumen breve
```python
def get_token():
    global _token, _token_expires

    if _token and time.time() < _token_expires - 30:
        return _token

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
```
- Cachea el token en memoria.
- Evita solicitudes innecesarias al backend de Spotify.
- Maneja vencimiento del token (expires_in).
  
## Búsquedas en Spotify

### Buscar artistas  
`GET /spotify/search?q=arctic+monkeys&type=artist`

### Buscar canciones  
`GET /spotify/search?q=uki&type=track`

## ⭐ Endpoint: Favoritos del Usuario
`GET /spotify/users/1/spotify/favorites`
Este endpoint:

- Obtiene preferencias del usuario de la db
- Busca el primer artista favorito en Spotify
- Obtiene sus top tracks
- Busca información detallada del segundo track favorito registrado del usuario

## Conclusiones y Observaciones
- El token de Spotify expira aproximadamente cada hora; el sistema implementa cache y renovación automática.
- La arquitectura separa CRUD, modelos, rutas y cliente externo, lo cual facilita mantenimiento y escalabilidad.
- Los modelos usan Pydantic (via SQLModel) para garantizar que datos inválidos nunca entren a la base de datos.
- La API maneja fallos externos (Spotify) mediante códigos HTTP apropiados.
- La estructura del proyecto permite agregar nuevos endpoints sin afectar los existentes.
- Los favoritos del usuario ilustran cómo combinar información interna (base de datos) con servicios externos (Spotify).
  
### URL
https://github.com/alevm569/Python-APIs
