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
```angular2html
cd app
uvicorn app:app --reload
```

## Methods
```check /docs```
