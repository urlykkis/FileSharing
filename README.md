# File Sharing

<b>Stack: FastAPI, AsyncPG (PostgreSQL)</b>


## Settings
create file app/data/config.py
```
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_BASE=
JWT_SECRET=
JWT_ALGORITHM=
SECRET_KEY=
```
create file docker-compose.yml
```
version: "3"
services:

  database:
    image: postgres:latest
    restart: always
    environment:
      - POSTGRES_USER=
      - POSTGRES_PASSWORD=
      - PORT=5432
      - POSTGRES_DB=
    ports:
      - "5432:5432"
  api:
    depends_on:
      - database
    stdin_open: true
    restart: always
    build: ./
    command: uvicorn app:app --host 0.0.0.0 --reload
    ports:
      - "8000:8000"
```

## Install
```
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

## Generate Secret Key
```
python3
import secrets
print(secrets.token_urlsafe(30))
```

## Run
```
docker-compose up
```

## Methods
```check /docs```
