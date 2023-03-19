from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis.strategies import text, dictionaries

from app.services.firebase import (
    get_firestore_document,
    set_firestore_document,
)


@settings(deadline=None)
@given(collection=text(), document=text(), data=dictionaries(keys=text(), values=text()))
async def test_set_firestore_document(collection: str, document: str, data: dict):
    with patch("app.services.firebase.db.collection") as mock_collection:
        mock_document = MagicMock()
        mock_collection.return_value.document.return_value = mock_document

        await set_firestore_document(collection, document, data)
        mock_document.set.assert_called_once_with(data)


@settings(deadline=None)
@given(collection=text(), document=text())
async def test_get_firestore_document(collection: str, document: str):
    with patch("app.services.firebase.db.collection") as mock_collection:
        mock_document = MagicMock()
        mock_document.get.return_value.exists = True
        mock_document.get.return_value.to_dict.return_value = {"example": "data"}
        mock_collection.return_value.document.return_value = mock_document

        result = await get_firestore_document(collection, document)
        assert result == {"example": "data"}
