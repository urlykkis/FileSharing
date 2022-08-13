from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from data.config import SECRET_KEY
from routes import users, core


app = FastAPI(
    title="File Sharing"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(core.router)
app.include_router(users.router)
