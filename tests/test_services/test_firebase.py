from typing import List, Dict
import functools
import pytest
from hypothesis import given, settings
from hypothesis.strategies import text, dictionaries
from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from pytest_mock import MockerFixture

from app.services.firebase import (
    get_firestore_document,
    set_firestore_document,
    get_firestore_collection_by_uid,
    get_firestore_documents_by_uid,
    authenticate_user
)

mock_db = {}
app = FastAPI()


@settings(deadline=None)
@given(collection=text(), document=text(), data=dictionaries(keys=text(), values=text()))
@pytest.mark.asyncio
async def test_set_firestore_document(mocker: MockerFixture, collection: str, document: str, data: dict):
    mock_document = mocker.MagicMock()
    mock_collection = mocker.patch("app.services.firebase.db.collection", return_value=mocker.MagicMock(document=mocker.MagicMock(return_value=mock_document)))

    await set_firestore_document(collection, document, data)
    mock_document.set.assert_called_once_with(data)
    mock_collection.assert_called_once_with(collection)


@settings(deadline=None)
@given(collection=text(), document=text())
@pytest.mark.asyncio
async def test_get_firestore_document(mocker: MockerFixture, collection: str, document: str):
    mock_document = mocker.MagicMock()
    mock_collection = mocker.patch("app.services.firebase.db.collection", return_value=mocker.MagicMock(document=mocker.MagicMock(return_value=mock_document)))
    mock_document.get.return_value.exists = True
    mock_document.get.return_value.to_dict.return_value = {"example": "data"}

    result = await get_firestore_document(collection, document)
    assert result == {"example": "data"}
    mock_collection.assert_called_once_with(collection)
    mock_document.get.assert_called_once()


async def mock_stream(collection: str, uid: str):
    data = mock_db.get(collection, {}).get(uid, [])
    for item in data:
        yield item


@pytest.fixture(autouse=True)
def setup_mock_db(monkeypatch):
    # Replace the original Firestore `query.stream` method with the `mock_stream` method
    monkeypatch.setattr("app.services.firebase.query.stream", mock_stream)


# Define the strategies for generating input values for the functions
collection_strategy = st.text(min_size=1, max_size=10)
uid_strategy = st.text(min_size=1, max_size=10)
limit_strategy = st.integers(min_value=1, max_value=100)
offset_strategy = st.integers(min_value=0, max_value=100)


@given(collection=collection_strategy, uid=uid_strategy)
@pytest.mark.asyncio
async def test_get_firestore_collection_by_uid(collection: str, uid: str):
    mock_db[collection] = {
        uid: [{"id": "doc1"}, {"id": "doc2"}, {"id": "doc3"}]
    }
    result = await get_firestore_collection_by_uid(collection, uid)
    assert isinstance(result, List)
    assert all(isinstance(doc_id, str) for doc_id in result)


@given(collection=collection_strategy, uid=uid_strategy, limit=limit_strategy, offset=offset_strategy)
@pytest.mark.asyncio
async def test_get_firestore_documents_by_uid(collection: str, uid: str, limit: int, offset: int):
    mock_db[collection] = {
        uid: [{"data": "doc1_data"}, {
            "data": "doc2_data"}, {"data": "doc3_data"}]
    }
    result = await get_firestore_documents_by_uid(collection, uid, limit, offset)
    assert isinstance
