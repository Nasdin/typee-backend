from unittest.mock import AsyncMock, patch

import pytest
from hypothesis import given, settings
from hypothesis.strategies import from_type

from app.api.safe_word import (
    is_word_safe_find_out_from_openai,
    is_word_safe_firestore,
    update_word_safe_firestore
)
from app.models.word_data import WordData


@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_is_word_safe_find_out_from_openai(word_data: WordData):
    with patch("app.api.safe_word.chat_completion", new_callable=AsyncMock) as mock_completion:
        mock_completion.return_value = "Yes"

        result = await is_word_safe_find_out_from_openai(word_data)
        assert result == True

@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_is_word_safe_firestore_found(word_data: WordData):
    with patch("app.api.safe_word.get_firestore_document", new_callable=AsyncMock) as mock_get_firestore_document:
        mock_get_firestore_document.return_value = {"is_safe": True}

        result = await is_word_safe_firestore(word_data)
        assert result == True

@settings(deadline=None)
@given(word_data=from_type(WordData))
async def test_is_word_safe_firestore_not_found(word_data: WordData):
    with patch("app.api.safe_word.get_firestore_document", new_callable=AsyncMock) as mock_get_firestore_document:
        mock_get_firestore_document.return_value = None

        with pytest.raises(IndexError):
            await is_word_safe_firestore(word_data)


@settings(deadline=None)
@given(word_data=from_type(WordData), is_safe=True)
async def test_update_word_safe_firestore(word_data: WordData, is_safe: bool):
    with patch("app.api.safe_word.set_firestore_document", new_callable=AsyncMock) as mock_set_firestore_document:
        await update_word_safe_firestore(word_data, is_safe)
        mock_set_firestore_document.assert_called_once_with("safe_words", word_data.word, {"is_safe": is_safe})