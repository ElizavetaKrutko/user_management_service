"""Testing endpoints defined in main."""
import pytest
from fastapi import status


@pytest.mark.anyio
class TestApp:
    """Test class for app info endpoints defined in main."""

    async def test_root(self, async_test_client):
        """Test if app is available."""
        res = await async_test_client.get("/api/v1/healthcheck")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {"message": "Ready to work!"}
