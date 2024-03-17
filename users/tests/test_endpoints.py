import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from api import app
from database.mariadb.connection import Connection
from general.config import get_config
from users.methods import User
from users.schemas import UserLoginRequest

config = get_config()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://localhost:17071/"
    ) as client:
        yield client


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


@pytest.fixture(scope="function")
async def login_user(request):
    user_credentials = {
        1: {
            "username_or_email": "admin@email.com",
            "password": "Admin123!",
        },
        2: {
            "username_or_email": "new_user@email.com",
            "password": "NewUser123!",
        },
        3: {
            "username_or_email": "user@email.com",
            "password": "User123!",
        },
    }
    return await User.login(
        UserLoginRequest(**user_credentials[request.param])
    )


@pytest.mark.anyio
async def test_login(
    prepare_db, async_client: AsyncClient
):
    login_data = {
        "username_or_email": "user@email.com",
        "password": "User123!",
    }
    response = await async_client.post("/users/login", json=login_data)
    assert response.status_code == 200
    assert response.cookies.get("token") is not None
    assert len(response.cookies.get("token")) == 36


@pytest.mark.anyio
async def test_read_user(
    prepare_db, async_client: AsyncClient
):
    response = await async_client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "Admin",
        "role": "admin",
        "profile_picture": None,
    }
    response = await async_client.get("/users/2")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "username": "NewUser",
        "role": "new_user",
        "profile_picture": None,
    }
    response = await async_client.get("/users/3")
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "username": "User",
        "role": "user",
        "profile_picture": None,
    }


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [1], indirect=True)
async def test_update_user_admin(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    user_data = {
        "username": "EditedUser",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
        "role": "admin",
    }
    response = await async_client.patch("/users/3", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [3], indirect=True)
async def test_update_user_self(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    user_data = {
        "username": "EditedUser",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    response = await async_client.patch("/users/3", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [2], indirect=True)
async def test_update_user_other(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    user_data = {
        "username": "EditedUser",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    response = await async_client.patch("/users/3", json=user_data)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [3], indirect=True)
async def test_update_user_not_admin(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    user_data = {
        "username": "EditedUser",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
        "role": "admin",
    }
    response = await async_client.patch("/users/3", json=user_data)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [1], indirect=True)
async def test_update_user_not_found(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    user_data = {
        "username": "EditedUser",
        "email": "edited_user@email.com",
        "password": "EditedUser123!",
    }
    response = await async_client.patch("/users/100", json=user_data)
    assert response.status_code == 404
    assert response.json() == {"error": "User not found"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [1], indirect=True)
async def test_delete_user_admin(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    response = await async_client.delete("/users/3")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [3], indirect=True)
async def test_delete_user_self(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    response = await async_client.delete("/users/3")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [2], indirect=True)
async def test_delete_user_other(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    response = await async_client.delete("/users/3")
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}


@pytest.mark.anyio
@pytest.mark.parametrize("login_user", [1], indirect=True)
async def test_delete_user_not_found(
    prepare_db, async_client: AsyncClient, login_user
):
    async_client.cookies.set("token", login_user)
    response = await async_client.delete("/users/100")
    assert response.status_code == 404
    assert response.json() == {"error": "User not found"}


@pytest.mark.anyio
async def test_create_user(
    prepare_db, async_client: AsyncClient
):
    user_data = {
        "username": "NewestUser",
        "email": "newest_user@email.com",
        "password": "NewestUser123!",
    }
    response = await async_client.post("/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created"}


@pytest.mark.anyio
async def test_search_user(
    prepare_db, async_client: AsyncClient
):
    response = await async_client.get("/users/?query=admin")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "username": "Admin",
            "role": "admin",
            "profile_picture": None,
        }
    ]
    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "username": "Admin",
            "role": "admin",
            "profile_picture": None,
        },
        {
            "id": 2,
            "username": "NewUser",
            "role": "new_user",
            "profile_picture": None,
        },
        {
            "id": 3,
            "username": "User",
            "role": "user",
            "profile_picture": None,
        },
    ]


@pytest.mark.anyio
async def test_confirm_user(
    prepare_db, async_client: AsyncClient
):
    response = await async_client.post("/users/confirm?token=new_user_token")
    assert response.status_code == 200
    assert response.json() == {"message": "User confirmed"}
