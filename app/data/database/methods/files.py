from asyncpg import Record
from datetime import datetime, timezone

from data.database.loader import db


async def register_file(fid: str, filename: str, uid: int, filesize: int,
                        auto_destroy: int = 0, qr_code: str = "text") -> None:
    await db.con.execute("INSERT INTO files (fid, filename, date_uploaded, uid, filesize, qr_code, auto_destroy) "
                         "VALUES ($1, $2, $3, $4, $5, $6, $7)",
                         fid, filename, datetime.now(), uid, filesize, qr_code, auto_destroy)


async def select_file(fid: str) -> Record:
    return await db.con.fetch("SELECT * FROM files WHERE fid = $1", fid)


async def update_file_downloads(fid: str, file_name: str) -> None:
    await db.con.execute("UPDATE files SET downloads = downloads + 1 WHERE fid = $1 AND filename = $2", fid, file_name)
