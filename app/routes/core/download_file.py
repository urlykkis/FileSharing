import os

from fastapi.responses import FileResponse

from .loader import router
from data.database.methods.files import update_file_downloads


@router.get("/{file_id}/{file_name}",
            name="Скачивание файла", status_code=200,
            description="Пользователь скачивает файл",
            response_description="Возвращает файл",
            response_class=FileResponse)
async def download_file(file_id: str, file_name: str):
    file_path = f"{os.getcwd()}/files/{file_id}/{file_name}"
    await update_file_downloads(file_id, file_name)
    return FileResponse(path=file_path, status_code=200, filename=file_name)
