import os

from fastapi.responses import FileResponse

from .loader import router
from data.database.methods.files import update_file_downloads
from utils.archive import archive_directory


@router.get("/{file_id}/{file_name}",
            name="Скачивание файла", status_code=200,
            description="Пользователь скачивает файл",
            response_description="Возвращает файл")
async def download_file(file_id: str, file_name: str) -> FileResponse:
    directory_path: str = f"{os.getcwd()}\\files\\{file_id}\\"

    if file_name != "all":
        file_path: str = directory_path + file_name
        await update_file_downloads(file_id, file_name)
        return FileResponse(path=file_path, status_code=200, filename=file_name)

    else:
        archive_file_name: str = file_id + ".zip"
        archive_path: str = directory_path + archive_file_name

        await archive_directory(archive_path, directory_path)
        file: FileResponse = FileResponse(path=archive_path, status_code=200, filename=archive_file_name)
        return file
