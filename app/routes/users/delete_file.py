from fastapi import Depends, HTTPException
from asyncpg import Record

from .loader import router

from utils.schemas.users import User
from utils.schemas.files import UpdateFile
from utils.dependencies import JWTBearer
from data.responses import Response, ResponseSchemas
from data.database.methods.files import get_file_uid, delete_file


@router.delete("/delete_file", status_code=200,
               name="Удаление файла пользователем",
               response_description="Файл удален",
               response_model=ResponseSchemas.FileEdited)
async def delete_file_handler(file: UpdateFile, user: User = Depends(JWTBearer())) \
        -> ResponseSchemas.FileEdited | HTTPException:
    db_file: Record = await get_file_uid(file.fid)

    if db_file:
        if db_file[0]["uid"] == user.uid:
            await delete_file(db_file.fid)
            return Response.file_deleted(db_file.fid)
        else:
            return Response.file_delete_not_allowed
    else:
        return Response.file_not_found
