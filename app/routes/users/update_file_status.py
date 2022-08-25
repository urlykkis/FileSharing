from fastapi import Depends, HTTPException
from asyncpg import Record

from .loader import router

from data.responses import Response, ResponseSchemas
from data.database.methods.files import get_file_uid, update_file_access
from utils.schemas.users import User
from utils.schemas.files import UpdateFile
from utils.dependencies import JWTBearer
from utils.validate import validate_user_file


@router.post("/update_file_access", status_code=200,
             name="Обновление статуса файла",
             response_description="Возвращает статус файла",
             response_model=ResponseSchemas.FileEdited)
async def update_file_access_handler(file: UpdateFile, user: User = Depends(JWTBearer())) \
        -> ResponseSchemas.FileEdited | HTTPException:
    db_file: Record = await get_file_uid(file.fid)
    validate_response: bool | HTTPException = await validate_user_file(db_file, user.uid)
    if isinstance(validate_response, bool):
        await update_file_access(file.fid)
        return Response.file_status_updated(file.fid)
    else:
        return validate_response

