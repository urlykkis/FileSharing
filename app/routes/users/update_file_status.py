from fastapi import Depends, HTTPException
from asyncpg import Record

from .loader import router

from utils.schemas.users import User
from utils.schemas.files import UpdateFile
from utils.dependencies import JWTBearer
from data.responses import Response, ResponseSchemas
from data.database.methods.files import get_file_uid, update_file_access


@router.post("/update_file_access", status_code=200,
             name="Обновление статуса файла",
             response_description="Возвращает статус файла",
             response_model=ResponseSchemas.FileEdited)
async def update_file_access_handler(file: UpdateFile, user: User = Depends(JWTBearer())) \
        -> ResponseSchemas.FileEdited | HTTPException:
    db_file: Record = await get_file_uid(file.fid)
    if db_file:
        if db_file[0]["uid"] == user.uid:
            await update_file_access(file.fid)
            return Response.file_status_updated(file.fid)
        else:
            return Response.file_delete_not_allowed
    else:
        return Response.file_not_found
