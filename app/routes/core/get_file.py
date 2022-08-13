from fastapi import Request, HTTPException
from asyncpg import Record

from .loader import router
from data.database.methods.files import select_file
from data.responses import Response, ResponseSchemas
from utils.functions import generate_data_files


@router.get("/{file_id}", name='Получить файл', status_code=200,
            description="Получает всю информацию об файле",
            response_description="Возвращает информация о файле")
async def get_file(request: Request, file_id: str) -> HTTPException | ResponseSchemas.FileFound:
    db_files: Record = await select_file(file_id)
    if db_files:
        data: dict = await generate_data_files(request, file_id, db_files)
        return Response.file_found(data)
    else:
        return Response.wrong_file_name
