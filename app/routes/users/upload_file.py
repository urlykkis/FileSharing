import os

from fastapi import UploadFile, Depends, HTTPException, Request, File
from json import loads
from random import choice
from string import ascii_letters

from .loader import router
from data.database.methods.files import register_file
from data.responses import Response, ResponseSchemas
from utils.schemas.users import User
from utils.schemas.files import file_data
from utils.dependencies import JWTBearer
from utils.functions import save_file


symbols = list(ascii_letters)


@router.put("/upload", name='Загрузка файла', status_code=201,
            description="Загрузка файла пользователем",
            response_description="Вовзращает идентификатор файла",
            response_model=ResponseSchemas.FileCreated)
async def upload_handler(files: list[UploadFile] = File(...), data: str = file_data,
                         user: User = Depends(JWTBearer())) -> HTTPException | ResponseSchemas.FileCreated:
    fid: str = "".join(choice(symbols) for _ in range(0, 11))
    try:
        data: dict = loads(data)
        auto_destroy: int = data["auto_destroy"]
    except:
        return HTTPException(status_code=404, detail="Проверьте аргументы")

    folder_path: str = rf"files/{fid}/"
    if os.path.exists(folder_path) is False:
        os.mkdir(folder_path)

    for file in files:
        if 500 >= len(file.filename) > 0:
            await save_file(folder_path + file.filename, file)
            file_size = len(await file.read())
            await register_file(fid, file.filename, user.uid, file_size, auto_destroy)

    return Response.file_created(fid)
