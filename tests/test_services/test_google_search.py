from hypothesis import given, settings
from hypothesis.strategies import text
import pytest

from app.services.google_search import get_image_from_google, upload_image_to_gcs


@settings(deadline=None)
@given(word=text(min_size=1))
@pytest.mark.asyncio
async def test_get_image_from_google(word: str, mocker):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"items": [{"link": "test_image_url"}]}

    result = await get_image_from_google(word)
    assert result == "test_image_url"
    mock_get.assert_called_once()


@settings(deadline=None)
@given(image_url=text())
@pytest.mark.asyncio
async def test_upload_image_to_gcs(image_url: str, mocker):
    mock_get = mocker.patch("app.services.google_search.requests.get")
    mock_get.return_value.content = b"image_data"
    mock_blob = mocker.patch("app.services.google_search.bucket.blob")
    mock_upload = mocker.MagicMock()
    mock_blob.return_value = mock_upload

    await upload_image_to_gcs(image_url)
    mock_upload.upload_from_string.assert_called_once_with(
        b"image_data", content_type="image/jpeg"
    )
    mock_get.assert_called_once_with(image_url, stream=True)    
