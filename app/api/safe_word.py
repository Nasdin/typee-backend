from google.cloud import firestore
import openai

db = firestore.Client()


async def is_word_safe_firestore(word_data: WordData):
    # Check if the word safety status is in Firestore
    doc_ref = db.collection("safe_words").document(word_data.word)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()["is_safe"]
    raise IndexError


async def update_word_safe_firestore(word_data: WordData, is_safe):
    doc_ref = db.collection("safe_words").document(word_data.word)
    doc_ref.set({"is_safe": is_safe})



async def is_word_safe_find_out_from_openai(word_data:WordData):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Is the word '{word_data.word}' safe for children?",
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.5,
    )

    result = response.choices[0].text.strip().lower()

    return result == "yes"



async def is_word_safe(word_data: WordData):
    # Integrates both firestore and openai

    try:
        is_safe = await is_word_safe_firestore(word_data)
        return is_safe
    except IndexError:
        # Call openAI instead to find out
        is_safe = await is_word_safe_find_out_from_openai(word_data)
        await update_word_safe_firestore(word_data, is_safe)
        return is_safe
    



