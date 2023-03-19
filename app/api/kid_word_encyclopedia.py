from app.models.word_data import WordData, WordInfo
from app.services.firebase import get_firestore_document, set_firestore_document
from app.services.google_search import upload_image_to_gcs, get_image_from_google
from app.services.openai import chat_completion


async def get_image_url_from_firebase(word_data: WordData) -> str:
    data = get_firestore_document("image_urls", word_data.word)
    if data:
        return data["image_url"]

    # If the image URL is not found in Firebase, get it from Google
    image_url = await get_image_from_google(word_data.word)

    # Upload the image to Google Cloud Storage
    gcs_image_path = await upload_image_to_gcs(image_url)

    # Update Firebase with the GCS image path
    set_firestore_document("image_urls", word_data.word, {"image_url": gcs_image_path})

    return gcs_image_path


async def generate_explanation(word_data: WordData) -> str:
    prompt = f"Explain the word '{word_data.word}' in a simple way that a 4-year-old child can understand."
    response = await chat_completion(prompt)
    return response.strip()


async def generate_story(word_data: WordData) -> str:
    prompt = f"Create a short and simple story for a 4-year-old child that includes the word '{word_data.word}'."
    response = await chat_completion(prompt)
    return response.strip()


async def generate_fact(word_data: WordData) -> str:
    prompt = f"Share an interesting and simple fact about the word '{word_data.word}' that a 4-year-old child would enjoy."
    response = await chat_completion(prompt)
    return response.strip()


async def kid_word_encyclopedia(word_data: WordData):
    data = get_firestore_document("word_data", word_data.word)

    if data:
        # Data found in Firestore, return as WordInfo object
        word_info = WordInfo(**data)
    else:
        # Data not found in Firestore, generate with OpenAI API
        # Call OpenAI API to generate imageUrl, explanation, story, and fact
        image_url_future = get_image_url_from_firebase(word_data)
        explanation_future = generate_explanation(word_data)
        story_future = generate_story(word_data)
        fact_future = generate_fact(word_data)

        # Await the results of the futures
        image_url = await image_url_future
        explanation = await explanation_future
        story = await story_future
        fact = await fact_future

        # Save generated data to Firestore
        data = {
            "imageUrl": image_url,
            "explanation": explanation,
            "story": story,
            "fact": fact,
        }
        set_firestore_document("word_data", word_data.word, data)

        # Create WordInfo object
        word_info = WordInfo(**data)

    return word_info
