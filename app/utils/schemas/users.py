from fastapi import HTTPException
from ipaddress import IPv4Address
from pydantic import BaseModel, validator, validate_email
from datetime import datetime, date

from data.responses import Response


class User(BaseModel):
    uid: int
    username: str
    email: str | None
    password: str
    reg_date: date | datetime | str
    reg_ip: str | IPv4Address
    status: bool
    is_admin: bool
    recent_entries: dict | str
    total_files: int

    @validator('reg_date')
    def __validate_reg_date(cls, reg_date) -> str:
        if isinstance(reg_date, date | datetime):
            reg_date: str = reg_date.strftime("%d.%m.%Y")
            return reg_date
        else:
            return reg_date

    @validator('reg_ip')
    def __validate_reg_ip(cls, reg_ip) -> str:
        if isinstance(reg_ip, IPv4Address):
            reg_ip: str = str(reg_ip)
            return reg_ip
        else:
            return reg_ip


class RegisterUser(BaseModel):
    username: str
    email: str | None
    password: str

    @validator('username')
    def __validate_username(cls, username) -> str | HTTPException:
        if 100 > len(username) < 0:
            return Response.username_wrong_length
        else:
            return username

    @validator('email')
    def __validate_email(cls, email) -> str | HTTPException | Response:
        if 150 > len(email) < 0:
            return Response.email_wrong_length
        else:
            if validate_email(email):
                return email
            else:
                raise Response.wrong_email

    @validator('password')
    def __validate_password(cls, password) -> str | HTTPException:
        if 150 > len(password) < 0:
            return Response.password_wrong_length
        else:
            return password


class AuthenticateUser(BaseModel):
    username: str
    password: str
