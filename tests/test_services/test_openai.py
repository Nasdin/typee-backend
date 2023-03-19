from unittest.mock import AsyncMock, MagicMock, patch

from hypothesis import given, settings
from hypothesis.strategies import text

from app.services.openai import chat_completion


@settings(deadline=None)
@given(prompt=text())
async def test_chat_completion(prompt: str):
    with patch("your_module.openai.ChatCompletion.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(message={"content": "test response"})])

        response = await chat_completion(prompt)
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        assert response == "test response"

