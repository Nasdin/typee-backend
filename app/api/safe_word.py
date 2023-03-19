from app.services.firebase import get_firestore_document, set_firestore_document
from app.services.google_search import chat_completion

async def is_word_safe_firestore(word_data: WordData):
    # Check if the word safety status is in Firestore
    data = get_firestore_document("safe_words", word_data.word)
    if data:
        return data["is_safe"]
    raise IndexError

async def update_word_safe_firestore(word_data: WordData, is_safe):
    set_firestore_document("safe_words", word_data.word, {"is_safe": is_safe})

async def is_word_safe_find_out_from_openai(word_data:WordData):
    prompt = f"Is the word '{word_data.word}' safe for children? Please answer yes or no."
    response = await chat_completion(prompt)
    result = response.strip().lower()
    return result == "yes" or result == "y"


async def is_word_safe(word_data: WordData):
    # Integrates both Firestore and OpenAI

    try:
        is_safe = await is_word_safe_firestore(word_data)
        return is_safe
    except IndexError:
        # Call OpenAI instead to find out
        is_safe = await is_word_safe_find_out_from_openai(word_data)
        await update_word_safe_firestore(word_data, is_safe)
        return is_safe
