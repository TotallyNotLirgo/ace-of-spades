from typing import Self

import aiomysql

from general.config import get_config

config = get_config()


class Connection:
    conn: aiomysql.Connection | None

    def __init__(self):
        self.conn = None

    async def cursor(self) -> aiomysql.Cursor:
        if not self.conn:
            raise aiomysql.DatabaseError("Not connected to the database")
        return await self.conn.cursor()

    async def __aenter__(self) -> Self:
        self.conn = await aiomysql.connect(
            host=config.MARIADB_HOST,
            user=config.MARIADB_USER,
            password=config.MARIADB_PASSWORD,
            db=config.MARIADB_DATABASE,
            autocommit=True,
        )
        return self

    async def __aexit__(self, *args, **kwargs):
        if self.conn:
            self.conn.close()
        self.conn = None
