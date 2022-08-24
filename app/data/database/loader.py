from asyncpg import connect
from asyncio import create_task

from data.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_BASE


class Database:
    def __init__(self, hostname, port, database, username, password):
        self.hostname = hostname
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        create_task(self.init())

    async def init(self) -> None:
        self.con = await connect(host=self.hostname, user=self.username,
                                 database=self.database, password=self.password,
                                 port=self.port)

        await self.con.execute("""CREATE TABLE IF NOT EXISTS users (
            uid serial NOT NULL UNIQUE PRIMARY KEY,
            username char(100),
            email char(150),
            password char(150),
            reg_date date,
            reg_ip inet,
            status boolean DEFAULT True,
            is_admin boolean DEFAULT False,
            recent_entries json,
            total_files smallint NOT NULL DEFAULT 0
        )""")

        await self.con.execute("""CREATE TABLE IF NOT EXISTS files (
            fid char(30) NOT NULL,
            filename char(500),
            date_uploaded timestamp,
            uid integer REFERENCES users (uid),
            downloads smallint DEFAULT 0,
            filesize integer,
            qr_code TEXT,
            auto_destroy integer DEFAULT 0,
            password char(30) DEFAULT NULL,
            access BOOLEAN DEFAULT TRUE
        )""")


db = Database(hostname=DB_HOST, port=DB_PORT, database=DB_BASE,
              username=DB_USER, password=DB_PASSWORD)
