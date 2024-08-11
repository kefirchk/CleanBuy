import pytest
from httpx import AsyncClient


async def test_response_validation_exception_handler(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": "fucker",
        "password": "1234",
        "role": "blablabla",
        "email": "alex@example.com",
        "buyer_information": None
    })
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'enum',
                'loc': ['body', 'role'],
                'msg': "Input should be 'USER' or 'BUYER'",
                'input': 'blablabla',
                'ctx': {
                    'expected': "'USER' or 'BUYER'"
                }
            }
        ]
    }


async def test_global_exception_handler(ac: AsyncClient):
    with pytest.raises(Exception):
        response = await ac.get("/non-existent-endpoint")
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error."}


@pytest.mark.asyncio
async def test_not_found_exception_handler(ac: AsyncClient):
    response = await ac.get("/users/-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Buyer not found"}
