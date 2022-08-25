from fastapi import HTTPException
from asyncpg import Record

from data.responses import Response
from data.database.methods.users import select_user_by_username, select_user_by_email
from utils.schemas.users import RegisterUser


async def validate_register_user(user: RegisterUser) -> bool | HTTPException:
    if await select_user_by_username(user.username):
        return Response.username_already_registered

    elif await select_user_by_email(user.email):
        return Response.email_already_registered

    else:
        return True


async def validate_user_file(db_file: Record, uid: int) -> bool | HTTPException:
    if db_file:
        if db_file[0]["uid"] == uid:
            return True
        else:
            return Response.file_delete_not_allowed
    else:
        return Response.file_not_found
