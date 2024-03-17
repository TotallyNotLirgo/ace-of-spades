from fastapi import HTTPException

from database.mariadb.connection import Connection
from aiomysql import IntegrityError

from .schemas import (
    UserLoginRequest,
    UserCreateRequest,
    UserReadResponse,
    UserUpdateRequest,
    UserAuth,
)
from .security import generate_token, hash_value
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class User:
    @staticmethod
    async def login(user: UserLoginRequest) -> str:
        """
        Login a user
        Args:
            user (UserLoginRequest): The user to login
        Returns:
            str: The token
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT id FROM user "
                "WHERE (username = %s OR email = %s) AND password = %s",
                (
                    user.username_or_email,
                    user.username_or_email,
                    hash_value(user.password),
                ),
            )
            user_data = await cursor.fetchone()
            if not user_data:
                raise HTTPException(401, "Invalid username, email or password")
            token = generate_token()
            await cursor.execute(
                "DELETE FROM session WHERE "
                "user_id = %s AND expiration < NOW()",
                (user_data[0],),
            )
            await cursor.execute(
                "INSERT INTO session (user_id, token, expiration) "
                "VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 1 HOUR))",
                (user_data[0], token),
            )
            return token

    @staticmethod
    async def authorize(token: str) -> UserAuth:
        """
        Authorize a user
        Args:
            token (str): The token
        Returns:
            int: The user id
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT user_id, expiration, NOW() FROM session "
                "WHERE token = %s AND expiration > NOW()",
                (token,),
            )
            user_data = await cursor.fetchone()
            if not user_data:
                raise HTTPException(401, "Invalid or expired token")
            if user_data[1] < user_data[2] + timedelta(minutes=15):
                await cursor.execute(
                    "UPDATE session SET "
                    "expiration = DATE_ADD(NOW(), INTERVAL 1 HOUR) "
                    "WHERE token = %s",
                    (token,),
                )
            await cursor.execute(
                "SELECT role FROM user WHERE id = %s", (user_data[0],)
            )
            role = (await cursor.fetchone())[0]
            return UserAuth(id=user_data[0], role=role)

    @staticmethod
    async def create(user: UserCreateRequest):
        """
        Create a user
        Args:
            user (UserCreateRequest): The user to create
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            try:
                await cursor.execute(
                    "INSERT INTO user "
                    "(username, password, email, role, created_at, updated_at) "
                    "VALUES (%s, %s, %s, 'new_user', NOW(), NOW())",
                    (user.username, hash_value(user.password), user.email),
                )
            except IntegrityError as e:
                if "username" in e.args[1]:
                    raise HTTPException(409, "Username already exists")
                if "email" in e.args[1]:
                    raise HTTPException(409, "Email already exists")
            token = generate_token()
            await cursor.execute(
                "INSERT INTO session (user_id, token, expiration) "
                "VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 1 HOUR))",
                (cursor.lastrowid, token),
            )
            logger.info(
                f"User created: {user.username} with assigned token {token}"
            )

    @staticmethod
    async def confirm(token: str):
        """
        Confirm a user
        Args:
            token (str): The token
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "UPDATE user SET role = 'user' "
                "WHERE id = (SELECT user_id FROM session WHERE token = %s)",
                (token,),
            )
            if cursor.rowcount == 0:
                raise HTTPException(404, "Token not found")

    @staticmethod
    async def search(query: str) -> list[UserReadResponse]:
        """
        Search for users
        Args:
            query (str): The search query
        Returns:
            list[UserReadResponse]: The users
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT id, username, role, profile_picture "
                "FROM user WHERE username LIKE %s ORDER BY id",
                (f"%{query}%",),
            )
            user_data = await cursor.fetchall()
            return [
                UserReadResponse(
                    id=user[0],
                    username=user[1],
                    role=user[2],
                    profile_picture=user[3],
                )
                for user in user_data
            ]

    @staticmethod
    async def read(user_id: int) -> UserReadResponse:
        """
        Read a user
        Args:
            user_id (int): The user id
        Returns:
            UserReadResponse: The user data
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "SELECT username, role, profile_picture "
                "FROM user WHERE id = %s",
                (user_id,),
            )
            user_data = await cursor.fetchone()
            if not user_data:
                raise HTTPException(404, "User not found")
            return UserReadResponse(
                id=user_id,
                username=user_data[0],
                role=user_data[1],
                profile_picture=user_data[2],
            )

    @staticmethod
    async def update(user_id: int, user: UserUpdateRequest):
        """
        Update a user
        Args:
            user_id (int): The user id
            user (UserUpdateRequest): The user data to update
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            try:
                await cursor.execute(
                    "UPDATE user SET "
                    "username = COALESCE(%s, username), "
                    "password = COALESCE(%s, password), "
                    "email = COALESCE(%s, email), "
                    "role = COALESCE(%s, role), "
                    "profile_picture = COALESCE(%s, profile_picture), "
                    "updated_at = NOW() "
                    "WHERE id = %s",
                    (
                        user.username,
                        hash_value(user.password) if user.password else None,
                        user.email,
                        user.role,
                        user.profile_picture,
                        user_id,
                    ),
                )
            except IntegrityError as e:
                if "username" in e.args[1]:
                    raise HTTPException(409, "Username already exists")
                if "email" in e.args[1]:
                    raise HTTPException(409, "Email already exists")
            if cursor.rowcount == 0:
                raise HTTPException(404, "User not found")

    @staticmethod
    async def delete(user_id: int):
        """
        Delete a user
        Args:
            user_id (int): The user id
        """
        async with Connection() as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                "DELETE FROM session WHERE user_id = %s", (user_id,)
            )
            await cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
            if cursor.rowcount == 0:
                raise HTTPException(404, "User not found")
