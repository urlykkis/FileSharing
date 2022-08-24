from fastapi import Depends, HTTPException
from asyncpg import Record

from .loader import router
from utils.schemas.users import User
from utils.schemas.files import FileBase
from utils.dependencies import JWTBearer
from data.responses import Response, ResponseSchemas
from data.database.methods.files import get_user_files


@router.get("/myfiles", status_code=200,
            name="Получение файлов пользователя",
            response_description="Возвращает ошибку или список файлов пользователя",
            response_model=ResponseSchemas.UserFiles)
async def user_files_handler(user: User = Depends(JWTBearer())) -> ResponseSchemas.UserFiles | HTTPException:
    user_files: list[Record] | None = await get_user_files(user.uid)
    if user_files is not None:
        files: dict = {
            "files": []
        }

        for file in user_files:
            file: dict = FileBase(**file).dict()
            file["fid"] = file["fid"].strip()
            file["filename"] = file["filename"].strip()
            file["password"] = file["password"].strip() if file["password"] is not None else None
            files["files"].append(file)

        return Response.user_files(files)
    else:
        return Response.user_files_not_found
