from hypothesis import given, strategies as st
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

# Test for the /is-word-safe route
@given(word=st.text(min_size=1))
def test_is_word_safe(word):
    response = client.post("/is-word-safe", json={"word": word})
    assert response.status_code in (200, 401)  # either a successful request or an unauthorized request

# Test for the /kid-word-encyclopedia route
@given(word=st.text(min_size=1))
def test_kid_word_encyclopedia(word):
    response = client.post("/kid-word-encyclopedia", json={"word": word})
    assert response.status_code in (200, 401)  # either a successful request or an unauthorized request
