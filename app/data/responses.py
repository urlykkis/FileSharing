from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from data.exceptions import ValidateEmailError


class ResponseSchemas:
    """Все ответные схемы"""

    class AuthenticatedUser(BaseModel):
        uid: int
        token: str

    class FileCreated(BaseModel):
        fid: str

    class FileFound(BaseModel):
        file_id: str
        files: list[dict]


class Response:
    """Все ответы"""

    ip_already_registered: HTTPException = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Вы уже зарегистрированы")

    email_already_registered: HTTPException = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Почта уже зарегистрирована")

    username_already_registered: HTTPException = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Логин уже зарегистрирован")

    username_wrong_length: HTTPException = HTTPException(
        status_code=status.HTTP_411_LENGTH_REQUIRED,
        detail="Неправильная длина логина"
    )

    email_wrong_length: HTTPException = HTTPException(
        status_code=status.HTTP_411_LENGTH_REQUIRED,
        detail="Неправильная длина почты"
    )

    password_wrong_length: HTTPException = HTTPException(
        status_code=status.HTTP_411_LENGTH_REQUIRED,
        detail="Неправильная длина пароля"
    )

    invalid_auth_scheme: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Неправильная схема аутентификации")

    invalid_user_token: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Невалидный токен")

    invalid_code_authorization: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Невалидный код авторизации")

    wrong_email: ValidateEmailError = ValidateEmailError(
        "Неправильная почта")

    user_not_found: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Пользователь не найден"
    )

    wrong_password: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неправильный пароль"
    )

    bad_file_size: HTTPException = HTTPException(
        status_code=status.HTTP_411_LENGTH_REQUIRED,
        detail="Слишком большой/маленький файл"
    )

    bad_file_name: HTTPException = HTTPException(
        status_code=status.HTTP_411_LENGTH_REQUIRED,
        detail="Название слишком длинное"
    )

    wrong_file_name: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Файл не найден"
    )

    @staticmethod
    def file_found(data: dict):
        return ResponseSchemas.FileFound(**data)

    @staticmethod
    def user_registered(uid: int, token: str) -> ResponseSchemas.AuthenticatedUser:
        return ResponseSchemas.AuthenticatedUser(**{"uid": uid, "token": token})

    @staticmethod
    def user_authenticated(uid: int, token: str) -> ResponseSchemas.AuthenticatedUser:
        return ResponseSchemas.AuthenticatedUser(**{"uid": uid, "token": token})

    @staticmethod
    def file_created(fid: str) -> ResponseSchemas.FileCreated:
        return ResponseSchemas.FileCreated(**{"fid": fid})
