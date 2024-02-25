from .connection import connect
from endpoints.schemas.general import APIError
from endpoints.security import generate_token
import sqlite3
import time


class User:
    @classmethod
    async def login(cls, email: str, password: str) -> tuple[str, int]:
        with connect() as con:
            cur = con.execute(
                "SELECT id FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            res = cur.fetchone()
            if res is None:
                raise APIError(401, "Invalid email or password")
            token: str | None = None
            while token is None:
                try:
                    token = generate_token()
                    expiration = int(time.time())
                    con.execute(
                        "UPDATE users "
                        "SET token = ?, expiration = ? "
                        "WHERE id = ?",
                        (token, expiration, res[0])
                    )
                    return token, expiration
                except sqlite3.IntegrityError:
                    token = None
