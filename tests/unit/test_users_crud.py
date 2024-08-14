from unittest.mock import MagicMock, patch, AsyncMock

import jwt
from httpx import AsyncClient

from src.users_crud.models import UserOrm
from src.users_crud.repositories import UserRepo
from src.users_crud.schemas import UserRead, UserUpdate


async def test_register(mocker, ac: AsyncClient, buyer_create_data):
    mock_create_user = mocker.patch(
        'src.users_crud.router.UserRepo.create_user',
        new_callable=AsyncMock,
        return_value=UserOrm(id=1)
    )
    response = await ac.post("/users/register", json=buyer_create_data)
    assert response.status_code == 201


async def test_get_me_success(ac: AsyncClient, user_orm_data):
    mock_get_user = AsyncMock()
    mock_get_user.return_value = AsyncMock(**user_orm_data)
    data = {"sub": "test_user"}
    test_token = jwt.encode(data, "secret_key", algorithm="HS256")
    with patch.object(UserRepo, 'get_user', mock_get_user):
        with patch("src.auth.config.auth_config.SECRET_KEY", "secret_key"):
            with patch("jwt.decode", return_value={"sub": "test_user"}):
                response = await ac.get("/users/me", headers={"Authorization": f"Bearer {test_token}"})

                assert response.status_code == 200
                assert response.json() == {
                    "id": 1,
                    "username": "test_user",
                    "email": "test@example.com",
                    "role": "USER",
                    "buyer_information": None
                }
                mock_get_user.assert_called_once_with(username="test_user")


async def test_get_me_error(ac: AsyncClient):
    mock_get_current_user = MagicMock()
    mock_get_current_user.return_value = UserRead(
        id=1,
        username="test_user",
        email="test@example.com",
        buyer_information=None
    )
    mock_get_current_user.side_effect = Exception("Unauthorized")

    response = await ac.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


async def test_get_user_success(ac: AsyncClient, user_orm_data):
    user_orm = UserOrm(**user_orm_data)
    with patch.object(UserRepo, 'get_user', return_value=user_orm):
        response = await ac.get("/users/1")

        assert response.status_code == 200
        assert response.json() == {
            "id": user_orm.id,
            "username": user_orm.username,
            "email": user_orm.email,
            "role": user_orm.role,
            "buyer_information": user_orm.buyer_information
        }


async def test_get_user_not_found(ac: AsyncClient):
    with patch.object(UserRepo, 'get_user', return_value=None):
        response = await ac.get("/users/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


async def test_get_users_success(mocker, ac: AsyncClient):
    def gen_user(user_id, username):
        return UserRead(
            id=user_id,
            username=username,
            email=f"{username}@example.com",
            role="USER",
            buyer_information=None
        )
    users = [gen_user(i, f"user{i}") for i in range(1, 3)]

    with patch.object(UserRepo, 'get_users', return_value=users):
        response = await ac.get("/users/all")
        assert response.status_code == 200
        assert response.json() == [
            user.model_dump()
            for user in users
        ]


async def test_get_users_not_found(ac: AsyncClient):
    with patch.object(UserRepo, 'get_users', return_value=[]):
        response = await ac.get("/users/all")

        assert response.status_code == 404
        assert response.json() == {"detail": "Users not found"}


async def test_update_user_success(ac: AsyncClient):
    user_update = UserUpdate(
        username="updated_user",
        email="updated_user@example.com",
        password="password",
        buyer_information=None
    )
    user_orm = UserOrm(
        id=1,
        username=user_update.username,
        role="USER",
        email=user_update.email,
        buyer_information=user_update.buyer_information
    )

    with patch.object(
            UserRepo,
            'update_user',
            return_value=user_orm
    ):
        response = await ac.put("/users/1", json=user_update.model_dump())

        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "user_id": user_orm.id
        }


async def test_update_user_not_found(ac: AsyncClient):
    user_update = UserUpdate(
        username="updated_user",
        email="updated_user@example.com",
        password="password",
        buyer_information=None
    )
    with patch.object(UserRepo, 'update_user', return_value=None):
        response = await ac.put("/users/1", json=user_update.model_dump())
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}


async def test_delete_user_success(ac: AsyncClient):
    user_id = 1
    with patch.object(UserRepo, 'delete_user', return_value=True):
        response = await ac.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "detail": "User deleted successfully"
        }


async def test_delete_user_not_found(ac: AsyncClient):
    user_id = 1
    with patch.object(UserRepo, 'delete_user', return_value=False):
        response = await ac.delete(f"/users/{user_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
