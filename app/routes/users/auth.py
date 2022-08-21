from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from asyncpg import Record

from .loader import router
from data.responses import ResponseSchemas, Response
from data.database.methods.users import select_user_by_username, update_user_recent_entries
from utils.schemas.users import AuthenticateUser
from utils.functions import sign_jwt, validate_password


@router.post('/auth', name='Авторизация', status_code=200,
             response_description="Возвращает токен пользователя",
             response_model=ResponseSchemas.AuthenticatedUser)
async def auth_handler(request: Request, user: AuthenticateUser) -> \
        HTTPException | JSONResponse | ResponseSchemas.AuthenticatedUser:
    db_user: Record | None = await select_user_by_username(user.username)

    if db_user:
        if validate_password(user.password, db_user[0]["password"].strip()):
            token: str = await sign_jwt(db_user[0]["uid"])
            platform: str | None = request.headers["sec-ch-ua-platform"] if request.headers.get("sec-ch-ua-platform") else None
            new_entry: dict = {
                request.client.host: {
                    "time:": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    "device": request.headers["user-agent"],
                    "platform": platform
                }}

            await update_user_recent_entries(db_user[0]["uid"], new_entry)
            return Response.user_authenticated(db_user[0]["uid"], token)
        else:
            return Response.wrong_password
    else:
        return Response.user_not_found
