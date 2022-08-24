import asyncio
import os

from datetime import datetime
from asyncpg import Record

from data.database.methods.files import get_files_with_auto_destroy, delete_file


def repeat_destroy_files(coro, lp) -> None:
    asyncio.ensure_future(coro(), loop=lp)
    lp.call_later(3600, repeat_destroy_files, coro, lp)


async def destroy_files() -> None:
    auto_destroy_files: Record = await get_files_with_auto_destroy()

    for file in auto_destroy_files:
        if datetime.strptime(file[1], "%d.%m.%Y %H:%M:%S") >= datetime.now():
            await delete_file(file[0])
            os.rmdir(f"./files/{file[0]}")
