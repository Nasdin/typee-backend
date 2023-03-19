from unittest.mock import AsyncMock, patch

from hypothesis import given, settings
from hypothesis.strategies import from_type

from app.api.kid_word_encyclopedia import (
    generate_fact,
    generate_explanation,
    generate_story,
    get_image_url_from_firebase
)
from app.models.word_data import WordData


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_generate_explanation(word_data: WordData):
    with patch("app.api.kid_word_encyclopedia.chat_completion", new_callable=AsyncMock) as mock_completion:
        mock_completion.return_value = "An apple is a fruit that is red, green, or yellow."

        result = await generate_explanation(word_data)
        assert result == "An apple is a fruit that is red, green, or yellow."


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_generate_story(word_data: WordData):
    with patch("app.api.kid_word_encyclopedia.chat_completion", new_callable=AsyncMock) as mock_completion:
        mock_completion.return_value = "Once upon a time, a little apple tree grew in a big forest."

        result = await generate_story(word_data)
        assert result == "Once upon a time, a little apple tree grew in a big forest."


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_generate_fact(word_data: WordData):
    with patch("app.api.kid_word_encyclopedia.chat_completion", new_callable=AsyncMock) as mock_completion:
        mock_completion.return_value = "Apples can float in water because they are 25% air."

        result = await generate_fact(word_data)
        assert result == "Apples can float in water because they are 25% air."


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_get_image_url_from_firebase_found(word_data: WordData):
    with patch("app.api.kid_word_encyclopedia.get_firestore_document",
               new_callable=AsyncMock) as mock_get_firestore_document:
        mock_get_firestore_document.return_value = {"image_url": "gs://test_bucket/image.jpg"}

        result = await get_image_url_from_firebase(word_data)
        assert result == "gs://test_bucket/image.jpg"


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_get_image_url_from_firebase_not_found(word_data: WordData):
    with patch("app.api.kid_word_encyclopedia.get_firestore_document",
               new_callable=AsyncMock) as mock_get_firestore_document:
        mock_get_firestore_document.return_value = None

        with patch("app.api.kid_word_encyclopedia.get_image_from_google",
                   new_callable=AsyncMock) as mock_get_image_from_google:
            mock_get_image_from_google.return_value = "https://example.com/image.jpg"

            with patch("app.api.kid_word_encyclopedia.upload_image_to_gcs",
                       new_callable=AsyncMock) as mock_upload_image_to_gcs:
                mock_upload_image_to_gcs.return_value = "gs://test_bucket/image.jpg"

                with patch("app.api.kid_word_encyclopedia.set_firestore_document",
                           new_callable=AsyncMock) as mock_set_firestore_document:
                    result = await get_image_url_from_firebase(word_data)

                    assert result == "gs://test_bucket/image.jpg"
                    mock_set_firestore_document.assert_called_once_with(
                        "image_urls", word_data.word, {"image_url": "gs://test_bucket/image.jpg"}
                    )
