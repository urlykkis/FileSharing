from fastapi import UploadFile, File, Form
from pydantic import BaseModel, validator, validate_email
from datetime import datetime, date

from data.responses import Response

file_data: Form = Form(default={"auto_destroy": 0})


class NewFile(BaseModel):
    auto_destroy: int = 0
