from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .functions import decode_jwt
from data.responses import Response
from data.database.methods.users import select_user_by_id
from utils.schemas.users import User


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> User | Response:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise Response.invalid_auth_scheme

            user: dict | None = self.verify_jwt(credentials.credentials)
            if not user:
                raise Response.invalid_user_token

            user = await select_user_by_id(user["user_id"])
            return User(**user[0])
        else:
            raise Response.invalid_code_authorization

    def verify_jwt(self, jwt_token: str) -> dict | None:
        try:
            payload = decode_jwt(jwt_token)
            return payload
        except:
            payload = None
            return payload
