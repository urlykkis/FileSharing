from fastapi import Depends, HTTPException
from asyncpg import Record

from .loader import router

from data.responses import Response, ResponseSchemas
from data.database.methods.files import get_file_uid, delete_file
from utils.schemas.users import User
from utils.schemas.files import UpdateFile
from utils.dependencies import JWTBearer
from utils.validate import validate_user_file


@router.delete("/delete_file", status_code=200,
               name="Удаление файла пользователем",
               response_description="Файл удален",
               response_model=ResponseSchemas.FileEdited)
async def delete_file_handler(file: UpdateFile, user: User = Depends(JWTBearer())) \
        -> ResponseSchemas.FileEdited | HTTPException:
    db_file: Record = await get_file_uid(file.fid)
    validate_response: bool | HTTPException = await validate_user_file(db_file, user.uid)

    if isinstance(validate_response, bool):
        if db_file[0]["uid"] == user.uid:
            await delete_file(db_file.fid)
            return Response.file_deleted(db_file.fid)
    else:
        return validate_response
