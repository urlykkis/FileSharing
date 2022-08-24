from fastapi import Form
from pydantic import BaseModel
from datetime import datetime

file_data: Form = Form(default={"auto_destroy": 0, "password": None, "access": True})


class FileBase(BaseModel):
    fid: str
    filename: str
    date_uploaded: str | datetime
    uid: int
    downloads: int
    filesize: int
    qr_code: str
    auto_destroy: int
    password: str | None
    access: bool


class UpdateFile(BaseModel):
    fid: str
