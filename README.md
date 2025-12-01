Python-APIs

API RESTful desarrollada con FastAPI, MySQL y Spotify Web API.

Proporciona funcionalidades para:

Gestión de usuarios

Registro y consulta de preferencias musicales

Integración con Spotify (búsquedas, top tracks, detalles)

Validación automática con Pydantic

Documentación interactiva mediante Swagger (/docs)

Estructura del Proyecto
music_api/
│── app/
│   ├── main.py                # Inicialización de la app + registro de rutas
│   ├── models.py              # Modelos SQLModel + validaciones Pydantic
│   ├── db.py                  # Conexión a MySQL + creación de tablas
│   ├── crud.py                # Lógica CRUD para usuarios y preferencias
│   ├── spotify_client.py      # Autenticación y peticiones a Spotify Web API
│   └── routers/
│       ├── users.py           # Endpoints CRUD de usuarios
│       ├── preferences.py     # Endpoints CRUD de preferencias
│       └── spotify.py         # Endpoints de integración con Spotify
│── requirements.txt
│── .env.example               # Variables de entorno requeridas
└── README.md

Instalación de Dependencias
pip install -r requirements.txt


Paquetes incluidos:

fastapi

uvicorn

sqlmodel

pymysql

requests

python-dotenv

Configuración de Variables de Entorno

Crear un archivo .env siguiendo esta estructura:

DB_HOST=localhost
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=music_api_db

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=

Configuración de la Base de Datos MySQL
CREATE DATABASE music_api_db;

CREATE USER 'music_user'@'%' IDENTIFIED BY 'tu_password';

GRANT ALL PRIVILEGES ON music_api_db.* TO 'music_user'@'%';

FLUSH PRIVILEGES;

Modelado de los Datos
Tabla User

id

username

email

full_name

Relación 1–N con preferencias

Tabla Preference

id

user_id

genre

favorite_artists (JSON)

favorite_tracks (JSON)
<img width="468" height="448" alt="image" src="https://github.com/user-attachments/assets/0f314772-3a20-4785-bbfc-8d90592fd29b" />

Endpoints
Usuarios

Crear usuario
POST /users/

{
  "username": "valery",
  "email": "valery@example.com",
  "full_name": "Valery Villarruel"
}


Listar usuarios
GET /users/

Obtener usuario por ID
GET /users/{id}

Actualizar usuario
PUT /users/{id}

Eliminar usuario
DELETE /users/{id}

Preferencias

Agregar preferencia
POST /users/{user_id}/preferences/

{
  "genre": "rock",
  "favorite_artists": ["Arctic Monkeys", "The Strokes"],
  "favorite_tracks": ["Do I Wanna Know", "505"]
}


Listar preferencias
GET /users/{user_id}/preferences/

Eliminar una preferencia
DELETE /users/{user_id}/preferences/{pref_id}

Integración con Spotify Web API

La API implementa:

Client Credentials Flow

Cache interno del token

Peticiones a https://api.spotify.com/v1/search

Toda la lógica se encuentra en app/spotify_client.py.

Búsquedas en Spotify

Buscar artistas
GET /spotify/search?q=arctic+monkeys&type=artist

Buscar canciones
GET /spotify/search?q=uki&type=track

Endpoint: Favoritos del Usuario

Este endpoint obtiene las preferencias musicales del usuario y realiza consultas automáticas a Spotify.

Usa el primer artista favorito para:

Buscarlo en Spotify

Obtener sus top tracks

Usa la segunda canción favorita para:

Buscar su información detallada en Spotify
