from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis.strategies import text

from app.services.google_search import get_image_from_google, upload_image_to_gcs


@settings(deadline=None)
@given(word=text(min_size=1))
async def test_get_image_from_google(word: str):
    with patch("your_module.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"items": [{"link": "test_image_url"}]}

        result = await get_image_from_google(word)
        assert result == "test_image_url"
        mock_get.assert_called_once()


@settings(deadline=None)
@given(image_url=text())
async def test_upload_image_to_gcs(image_url: str):
    with patch("app.services.google_search.requests.get") as mock_get:
        mock_get.return_value.content = b"image_data"
        with patch("app.services.google_search.bucket.blob") as mock_blob:
            mock_upload = MagicMock()
            mock_blob.return_value = mock_upload

            await upload_image_to_gcs(image_url)
            mock_upload.upload_from_string.assert_called_once_with(
                b"image_data", content_type="image/jpeg"
            )
