import asyncio
import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from data.config import SECRET_KEY, LOGS_PATH
from routes import users, core

logging.basicConfig(filename=LOGS_PATH,
                    filemode="a+",
                    format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt="%H:%M:%S")


app = FastAPI(title="File Sharing")


@app.middleware("http")
async def add_process_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(users.router)
app.include_router(core.router)


@app.on_event("startup")
async def on_startup():
    from utils.auto_delete_files import repeat_destroy_files, destroy_files
    loop = asyncio.get_event_loop()
    loop.call_later(1, repeat_destroy_files, destroy_files, loop)
