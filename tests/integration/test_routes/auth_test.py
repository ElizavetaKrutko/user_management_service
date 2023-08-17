import pytest
from fastapi import status

from app.common.config import logger


@pytest.mark.anyio
class TestAuthRoutes:
    """Test class for auth endpoints."""

    async def test_create_user_ok(
        self,
        async_test_client,
        user3_create,
        user3_in_db_schema,
        monkeypatch,
    ):
        res = await async_test_client.post("/api/v1/auth/signup", json=user3_create)

        logger.debug(res.json())
        pytest.access_token = res.json()["access_token"]
        pytest.refresh_token = res.json()["refresh_token"]

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["access_token"] != ""

    async def test_login_user_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        res = await async_test_client.post(
            "/api/v1/auth/login",
            json={"login": "test_user3", "password": "test_user3_password"},
        )

        logger.debug(res.json())
        pytest.access_token = res.json()["access_token"]
        pytest.refresh_token = res.json()["refresh_token"]

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["access_token"] != ""

    async def test_login_user_incorrect_login(
        self,
        async_test_client,
        monkeypatch,
    ):
        res = await async_test_client.post(
            "/api/v1/auth/login",
            json={"login": "test_user333", "password": "test_user3_password"},
        )

        logger.debug(res.json())

        assert res.json()["detail"] == "Incorrect login"

    async def test_refresh_token_could_not_validate(
        self,
        async_test_client,
        monkeypatch,
    ):
        refresh_token_incorrect = pytest.refresh_token.replace(
            pytest.refresh_token[len(pytest.refresh_token) - 1 :], "k2"
        )

        auth_header = "Bearer token".replace("token", refresh_token_incorrect)

        logger.debug(auth_header)

        res = await async_test_client.post(
            "/api/v1/auth/refresh-token", headers={"Authorization": auth_header}
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert res.json()["detail"] == "Could not validate credentials"

    async def test_refresh_token_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.refresh_token)

        logger.debug(auth_header)

        res = await async_test_client.post(
            "/api/v1/auth/refresh-token", headers={"Authorization": auth_header}
        )

        logger.debug(res.json())
        # pytest.access_token = res.json()["access_token"]
        pytest.refresh_token = res.json()["refresh_token"]

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["access_token"] != ""

    async def test_logout_user_token_blacklisted(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)

        res = await async_test_client.post(
            "/api/v1/auth/logout", headers={"Authorization": auth_header}
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert res.json()["detail"] == "Token blacklisted"

    async def test_login_seeded_user_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        res = await async_test_client.post(
            "/api/v1/auth/login",
            json={"login": "test_user2", "password": "test_user2_password"},
        )

        logger.debug(res.json())
        pytest.access_token = res.json()["access_token"]
        pytest.refresh_token = res.json()["refresh_token"]

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["access_token"] != ""
