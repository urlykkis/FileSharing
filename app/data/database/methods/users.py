from asyncpg import Record
from datetime import datetime
from json import loads, dumps

from data.database.loader import db


async def register_user(username: str, email: str | None, password: str,
                        reg_date: datetime, reg_ip: str, recent_entries: str) -> int:
    return await db.con.execute("INSERT INTO users (username, email, password, reg_date, reg_ip, recent_entries) "
                                "VALUES ($1, $2, $3, $4, $5, $6) RETURNING uid;",
                                username, email, password, reg_date, reg_ip, recent_entries)


async def select_user_by_username(username: str) -> Record | None:
    return await db.con.fetch("SELECT * FROM users WHERE username = $1", username)


async def select_user_by_reg_ip(reg_ip: str) -> Record | None:
    return await db.con.fetch("SELECT * FROM users WHERE reg_ip = $1", reg_ip)


async def select_user_by_email(email: str) -> Record | None:
    return await db.con.fetch("SELECT * FROM users WHERE email = $1", email)


async def select_user_by_id(uid: int) -> Record | None:
    return await db.con.fetch("SELECT * FROM users WHERE uid = $1", uid)


async def get_user_recent_entries(uid: int) -> dict:
    recent_entries = await db.con.fetchrow("SELECT recent_entries FROM users WHERE uid = $1", uid)
    if recent_entries[0] is None:
        recent_entries = '{}'
    else:
        recent_entries = recent_entries[0]
    return loads(recent_entries)


async def update_user_recent_entries(uid: int, entries: dict) -> None:
    recent_entries = await get_user_recent_entries(uid)
    recent_entries.update(entries)
    recent_entries = dumps(recent_entries)
    await db.con.execute("UPDATE users SET recent_entries = $1 WHERE uid = $2", recent_entries, uid)


async def update_user_total_files(uid: int) -> None:
    await db.con.execute("UPDATE users SET total_files = total_files + 1 WHERE uid = $1", uid)
