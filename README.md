# Python-APIs
API RESTful desarrollada con FastAPI, MySQL y Spotify Web API, que permite:

Gestionar usuarios

Registrar preferencias musicales

Consultar información desde Spotify (búsquedas + top tracks + detalles)

Validación automática usando Pydantic

Documentación interactiva mediante Swagger (/docs)
# Estructura del Proyecto
music_api/
│── app/
│   ├── main.py                # Inicialización de la app + registros de rutas
│   ├── models.py              # Modelos SQLModel + Pydantic
│   ├── db.py                  # Conexión a MySQL + creación de tablas
│   ├── crud.py                # Lógica CRUD de usuarios y preferencias
│   ├── spotify_client.py      # Autenticación + llamadas a Spotify Web API
│   └── routers/
│       ├── users.py           # Endpoints CRUD de usuarios
│       ├── preferences.py     # Endpoints CRUD de preferencias
│       └── spotify.py         # Endpoints de integración con Spotify
│── requirements.txt
│── .env.example               # Variables necesarias
└── README.md

# Instalación de dependencias
pip install -r requirements.txt

# Configuraciones de ambiente
DB_HOST=localhost
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=music_api_db

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=

# Creación db MySQL
CREATE DATABASE music_api_db;
CREATE USER 'music_user'@'%' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON music_api_db.* TO 'music_user'@'%';
FLUSH PRIVILEGES;

# Modelado de los datos
<img width="468" height="448" alt="image" src="https://github.com/user-attachments/assets/0f314772-3a20-4785-bbfc-8d90592fd29b" />
