import pytest

from fastapi import HTTPException
from database.mariadb.connection import Connection
from general.config import get_config
from users.methods import User
from users.schemas import (
    UserLoginRequest,
    UserCreateRequest,
    UserReadResponse,
    UserUpdateRequest,
)

config = get_config()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def prepare_db():
    async with Connection() as con:
        cur = await con.cursor()
        with open("initialize_test.sql", "r") as sql_file:
            sql_statements = sql_file.read()
        queries = sql_statements.split(";")
        for query in queries:
            if not query.strip():
                continue
            await cur.execute(query)


@pytest.mark.anyio
async def test_login_with_email(prepare_db):
    user_credentials = {
        "username_or_email": "user@email.com",
        "password": "User123!",
    }
    token = await User.login(UserLoginRequest(**user_credentials))
    assert token is not None
    assert len(token) == 36


@pytest.mark.anyio
async def test_login_with_username(prepare_db):
    user_credentials = {
        "username_or_email": "User",
        "password": "User123!",
    }
    token = await User.login(UserLoginRequest(**user_credentials))
    assert token is not None
    assert len(token) == 36


@pytest.mark.anyio
async def test_login_with_invalid_email(prepare_db):
    user_credentials = {
        "username_or_email": "invalid_email",
        "password": "User123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.login(UserLoginRequest(**user_credentials))

        assert err.status_code == 401
        assert err.detail == "Invalid username, email or password"


@pytest.mark.anyio
async def test_login_with_invalid_password(prepare_db):
    user_credentials = {
        "username_or_email": "User",
        "password": "invalid_password",
    }
    with pytest.raises(HTTPException) as err:
        await User.login(UserLoginRequest(**user_credentials))

        assert err.status_code == 401
        assert err.detail == "Invalid username, email or password"


@pytest.mark.anyio
async def test_register_user(prepare_db):
    user_data = {
        "username": "newest_user",
        "email": "newest_user@email.com",
        "password": "NewestUser123!",
    }
    await User.create(UserCreateRequest(**user_data))
    users: list[UserReadResponse] = await User.search("newest_user")
    assert len(users) == 1
    assert users[0].id == 4
    assert users[0].username == "newest_user"
    assert users[0].role == "new_user"


@pytest.mark.anyio
async def test_register_user_with_existing_email(prepare_db):
    user_data = {
        "username": "newest_user",
        "email": "new_user@email.com",
        "password": "NewestUser123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.create(UserCreateRequest(**user_data))

        assert err.status_code == 409
        assert err.detail == "Email already exists"


@pytest.mark.anyio
async def test_register_user_with_existing_username(prepare_db):
    user_data = {
        "username": "user",
        "email": "new_user@email.com",
        "password": "NewestUser123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.create(UserCreateRequest(**user_data))

        assert err.status_code == 409
        assert err.detail == "Username already exists"


@pytest.mark.anyio
async def test_confirm_user(prepare_db):
    await User.confirm("new_user_token")
    users: list[UserReadResponse] = await User.search("NewUser")
    assert len(users) == 1
    assert users[0].id == 2
    assert users[0].username == "NewUser"
    assert users[0].role == "user"


@pytest.mark.anyio
async def test_confirm_user_not_found(prepare_db):
    with pytest.raises(HTTPException) as err:
        await User.confirm("invalid_token")

        assert err.status_code == 404
        assert err.detail == "Token not found"


@pytest.mark.anyio
async def test_confirm_user_already_confirmed(prepare_db):
    with pytest.raises(HTTPException) as err:
        await User.confirm("user_token")

        assert err.status_code == 409
        assert err.detail == "User already confirmed"


@pytest.mark.anyio
async def test_update_user(prepare_db):
    user_data = {
        "username": "edited_user",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    await User.update(1, UserUpdateRequest(**user_data))
    users: list[UserReadResponse] = await User.search("edited_user")
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].username == "edited_user"
    assert users[0].role == "admin"


@pytest.mark.anyio
async def test_update_user_with_existing_email(prepare_db):
    user_data = {
        "username": "edited_user",
        "email": "user@email.com",
        "password": "EditedUser123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.update(1, UserUpdateRequest(**user_data))

        assert err.status_code == 409
        assert err.detail == "Email already exists"


@pytest.mark.anyio
async def test_update_user_with_existing_username(prepare_db):
    user_data = {
        "username": "user",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.update(1, UserUpdateRequest(**user_data))

        assert err.status_code == 409
        assert err.detail == "Username already exists"


@pytest.mark.anyio
async def test_update_user_not_found(prepare_db):
    user_data = {
        "username": "edited_user",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    with pytest.raises(HTTPException) as err:
        await User.update(100, UserUpdateRequest(**user_data))

        assert err.status_code == 404
        assert err.detail == "User not found"


@pytest.mark.anyio
async def test_update_user_with_partial_data(prepare_db):
    user_data = {
        "username": "edited_user",
    }
    await User.update(1, UserUpdateRequest(**user_data))
    users: list[UserReadResponse] = await User.search("edited_user")
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].username == "edited_user"
    assert users[0].role == "admin"


@pytest.mark.anyio
async def test_search_user(prepare_db):
    users: list[UserReadResponse] = await User.search("user")
    assert len(users) == 2
    assert users[0].id == 2
    assert users[0].username == "NewUser"
    assert users[0].role == "new_user"
    assert users[1].id == 3
    assert users[1].username == "User"
    assert users[1].role == "user"


@pytest.mark.anyio
async def test_search_user_not_found(prepare_db):
    users: list[UserReadResponse] = await User.search("invalid_user")
    assert len(users) == 0


@pytest.mark.anyio
async def test_search_user_empty(prepare_db):
    users: list[UserReadResponse] = await User.search("")
    assert len(users) == 3
    assert users[0].id == 1
    assert users[0].username == "Admin"
    assert users[0].role == "admin"
    assert users[1].id == 2
    assert users[1].username == "NewUser"
    assert users[1].role == "new_user"
    assert users[2].id == 3
    assert users[2].username == "User"
    assert users[2].role == "user"


@pytest.mark.anyio
async def test_read_user(prepare_db):
    user: UserReadResponse = await User.read(1)
    assert user.id == 1
    assert user.username == "Admin"
    assert user.role == "admin"


@pytest.mark.anyio
async def test_read_user_not_found(prepare_db):
    with pytest.raises(HTTPException) as err:
        await User.read(100)

        assert err.status_code == 404
        assert err.detail == "User not found"


@pytest.mark.anyio
async def test_delete_user(prepare_db):
    await User.delete(1)
    users: list[UserReadResponse] = await User.search("admin")
    assert len(users) == 0


@pytest.mark.anyio
async def test_delete_user_not_found(prepare_db):
    with pytest.raises(HTTPException) as err:
        await User.delete(100)

        assert err.status_code == 404
        assert err.detail == "User not found"
