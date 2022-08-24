import random
import string
import hashlib
import time
import jwt
import shutil

from asyncpg import Record
from fastapi import Request, UploadFile

from data.config import JWT_SECRET, JWT_ALGORITHM


def get_random_string(length: int = 12) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt: str = get_random_string()
    enc: bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def sign_jwt(user_id: int) -> str:
    payload: dict = {"user_id": user_id,
                     "expired": time.time() + 3600}
    token: str = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token: dict = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expired"] >= time.time() else None
    except:
        return {}


async def save_file(path: str, file: UploadFile) -> None:
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


async def generate_data_files(request: Request, file_id: str, db_files: Record) -> dict:
    data: dict = {
        "file_id": file_id,
        "files": [],
    }

    for file in db_files:
        file_data: dict = {
            "file_name": file[1].strip(),
            "date_uploaded": file[2].strftime("%d.%m.%Y %H:%M:%S"),
            "uid": file[3],
            "downloads": file[4],
            "file_size": file[5],
            "auto_destroy": file[6],
            "download_url": request.url.netloc + f"/{file_id}/{file[1].strip()}"
        }
        data["files"].append(file_data)

    return data
