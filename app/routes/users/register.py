from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from json import dumps

from .loader import router
from data.database.methods.users import register_user
from data.responses import Response, ResponseSchemas
from utils.schemas.users import RegisterUser
from utils.validate import validate_register_user
from utils.functions import hash_password, get_random_string, sign_jwt


@router.put('/register', name='Регистрация пользователя', status_code=201,
            response_description='Возвращает токен пользователя',
            response_model=ResponseSchemas.AuthenticatedUser)
async def register_handler(user: RegisterUser, request: Request) -> \
        str | JSONResponse | ResponseSchemas.AuthenticatedUser:
    response: str | bool = await validate_register_user(user, request.client.host)

    if response is True:
        salt: str = get_random_string()
        hashed_password: str = hash_password(user.password, salt)
        recent_entries: dict = {
            request.client.host: {
                "time:": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "device": request.headers["user-agent"],
                "platform": request.headers["sec-ch-ua-platform"]
            }}

        uid: int = await register_user(user.username, user.email, f"{salt}${hashed_password}",
                                       datetime.now(timezone.utc), request.client.host, dumps(recent_entries))
        token: str = await sign_jwt(uid)

        return Response.user_registered(uid, token)
    else:
        return response
