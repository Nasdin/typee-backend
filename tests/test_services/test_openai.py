from hypothesis import given, settings
from hypothesis.strategies import text
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
import openai
import httpx

from app.services.openai import chat_completion


@settings(deadline=None)
@given(prompt=text())
@pytest.mark.asyncio
async def test_chat_completion(prompt: str, mocker):
    mock_post = mocker.patch(
        "app.services.openai.httpx.AsyncClient.post", new_callable=mocker.AsyncMock)
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"choices": [{"text": "test response"}]}
    mock_post.return_value = mock_response

    response = await chat_completion(prompt)
    mock_post.assert_called_once_with(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        },
        headers={"Authorization": f"Bearer {openai.api_key}"}
    )
    assert response == "test response"


@settings(deadline=None)
@given(prompt=text())
@pytest.mark.asyncio
async def test_chat_completion_error(prompt: str, mocker):
    mock_post = mocker.patch(
        "app.services.openai.httpx.AsyncClient.post", new_callable=mocker.AsyncMock)
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Test Error")
    mock_post.return_value = mock_response

    with pytest.raises(httpx.HTTPStatusError):
        response = await chat_completion(prompt)
