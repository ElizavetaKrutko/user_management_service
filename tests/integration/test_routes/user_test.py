import pytest
from fastapi import status

from app.common.config import logger


@pytest.mark.anyio
class TestUserRoutes:
    """Test class for user endpoints."""

    async def test_get_user_me_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)
        logger.debug(auth_header)

        res = await async_test_client.get(
            "/api/v1/user/me", headers={"Authorization": auth_header}
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["username"] == "test_user2"

    async def test_patch_user_me_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)
        logger.debug(auth_header)

        res = await async_test_client.patch(
            "/api/v1/user/me",
            json={"name": "katya"},
            headers={"Authorization": auth_header},
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["name"] != ""
        assert res.json()["name"] == "katya"

    async def test_get_another_user_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)
        logger.debug(auth_header)

        res = await async_test_client.get(
            "/api/v1/user/1b417945-c927-439b-a3bd-8200847e2ef5",
            headers={"Authorization": auth_header},
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["username"] == "test_user1"

    async def test_patch_another_user_ok(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)
        logger.debug(auth_header)

        res = await async_test_client.patch(
            "/api/v1/user/1b417945-c927-439b-a3bd-8200847e2ef5",
            json={"surname": "ivanova"},
            headers={"Authorization": auth_header},
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_200_OK
        assert res.json()["surname"] == "ivanova"

    async def test_patch_another_user_not_found(
        self,
        async_test_client,
        monkeypatch,
    ):
        auth_header = "Bearer token".replace("token", pytest.access_token)
        logger.debug(auth_header)

        res = await async_test_client.patch(
            "/api/v1/user/1b417945-c927-439b-a3bd-8200847e2ef6",
            json={"surname": "ivanova"},
            headers={"Authorization": auth_header},
        )

        logger.debug(res.json())

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.json()["detail"] == "Could not find user"
