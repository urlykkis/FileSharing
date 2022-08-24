from asyncpg import Record
from datetime import datetime, timezone

from data.database.loader import db


async def register_file(fid: str, filename: str, uid: int, filesize: int,
                        password: str, access: bool,
                        auto_destroy: int = 0, qr_code: str = "text") -> None:
    await db.con.execute("INSERT INTO files "
                         "(fid, filename, date_uploaded, uid, filesize, qr_code, auto_destroy, password, access) "
                         "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)",
                         fid, filename, datetime.now(), uid, filesize, qr_code, auto_destroy, password, access)


async def select_file(fid: str) -> Record:
    return await db.con.fetch("SELECT * FROM files WHERE fid = $1", fid)


async def update_file_downloads(fid: str, file_name: str) -> None:
    await db.con.execute("UPDATE files SET downloads = downloads + 1 WHERE fid = $1 AND filename = $2", fid, file_name)


async def get_files_with_auto_destroy() -> Record:
    return await db.con.fetch("SELECT fid, date_uploaded FROM files WHERE auto_destroy > 0")


async def delete_file(fid: str) -> None:
    await db.con.execute("DELETE FROM files WHERE fid = $1", fid)


async def get_user_files(uid: int) -> list[Record] | None:
    return await db.con.fetch("SELECT * FROM files WHERE uid = $1", uid)


async def get_file_uid(fid: str) -> Record:
    return await db.con.fetch("SELECT uid FROM files WHERE fid = $1", fid)


async def update_file_access(fid: str) -> None:
    await db.con.execute("UPDATE files SET access = not access WHERE fid = $1", fid)
