from unittest.mock import MagicMock, patch
import functools
from typing import List, Dict
import pytest
from hypothesis import given, settings
from hypothesis.strategies import text, dictionaries
from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request

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
        mock_document.get.return_value.to_dict.return_value = {
            "example": "data"}
        mock_collection.return_value.document.return_value = mock_document

        result = await get_firestore_document(collection, document)
        assert result == {"example": "data"}


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
async def test_get_firestore_collection_by_uid(collection: str, uid: str):
    mock_db[collection] = {
        uid: [{"id": "doc1"}, {"id": "doc2"}, {"id": "doc3"}]
    }
    result = await get_firestore_collection_by_uid(collection, uid)
    assert isinstance(result, List)
    assert all(isinstance(doc_id, str) for doc_id in result)


@given(collection=collection_strategy, uid=uid_strategy, limit=limit_strategy, offset=offset_strategy)
async def test_get_firestore_documents_by_uid(collection: str, uid: str, limit: int, offset: int):
    mock_db[collection] = {
        uid: [{"data": "doc1_data"}, {
            "data": "doc2_data"}, {"data": "doc3_data"}]
    }
    result = await get_firestore_documents_by_uid(collection, uid, limit, offset)
    assert isinstance(result, List)
    assert all(isinstance(doc, Dict) for doc in result)
    assert len(result) <= limit

# Mock the verify_id_token function


def mock_verify_id_token(token: str):
    if token == "valid_token":
        return {"uid": "test_uid"}
    else:
        raise ValueError("Invalid token")


# Mock the request object
def mock_request(headers: Dict[str, str]) -> Request:
    request = MagicMock(spec=Request)
    request.headers = headers
    return request


@pytest.mark.parametrize(
    "headers, expected_status_code, expected_response",
    [
        ({"Authorization": "Bearer valid_token"}, 200, {"result": "success"}),
        ({"Authorization": "Bearer invalid_token"}, 401, {"error": "Unauthorized"}),
        ({}, 401, {"error": "Unauthorized"}),
    ],
)
def test_authenticate_user(headers, expected_status_code, expected_response):
    # Patch the auth.verify_id_token function with the mock function
    with unittest.mock.patch("app.services.firebase.auth.verify_id_token", mock_verify_id_token):
        # Use the authenticate_user decorator on a test endpoint
        @app.get("/test_auth")
        @authenticate_user()
        async def test_auth_endpoint(request: Request, uid: str = None):
            return {"result": "success"}

        # Test the endpoint using the TestClient
        client = TestClient(app)
        response = client.get("/test_auth", headers=headers)
        assert response.status_code == expected_status_code
        assert response.json() == expected_response
