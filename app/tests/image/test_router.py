from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app  # Ensure your FastAPI main app is importable

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.image.utils.fetch_and_prepare_image")
@patch("app.image.utils.is_valid_colormap")
async def test_get_image_frame_no_data(
    mock_is_valid_colormap, mock_fetch_and_prepare_image
):
    mock_is_valid_colormap.return_value = True  # Assuming the colormap is valid
    mock_fetch_and_prepare_image.return_value = None  # Simulate no data found

    with TestClient(app) as client:
        response = client.get(
            "/image-frame/", params={"depth_min": 5.0, "depth_max": 15.0}
        )
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.json())
        assert response.status_code == 404
        assert "No image rows found" in response.json()["detail"]
