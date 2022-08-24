# File Sharing

<b>Stack: FastAPI, AsyncPG (PostgreSQL), Docker</b>


## Settings
create file app/data/config.py
```
DB_HOST = ""
DB_PORT = 
DB_USER = ""
DB_PASSWORD = ""
DB_BASE = ""
JWT_SECRET = ""
JWT_ALGORITHM = ""
SECRET_KEY = ""
LOGS_PATH = ""
```
change docker-compose.yml

## Standart Settings
```
DB_HOST = "docker.for.mac.host.internal"
DB_PORT = 5432
DB_USER = "postgres"
DB_BASE = "filesharing"
JWT_ALGORITHM = "HS256"
LOGS_PATH = "./data/logs/logs.txt"
```

## Generate Secret Key
```
python3
import secrets
print(secrets.token_urlsafe(30))
```

## Install & Run
```
docker-compose up
```

## Methods
```check /docs```
