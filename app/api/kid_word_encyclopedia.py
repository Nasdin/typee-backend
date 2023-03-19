from app.services.firebase import get_firestore_document, set_firestore_document
from app.services.gcs import upload_blob, download_blob
from app.services.google_search import chat_completion

async def get_image_url_from_firebase(word: str) -> str:
    data = get_firestore_document("image_urls", word)
    if data:
        return data["image_url"]
    
    # If the image URL is not found in Firebase, get it from Google
    image_url = await get_image_from_google(word)

    # Upload the image to Google Cloud Storage
    gcs_image_path = await upload_image_to_gcs(image_url)

    # Update Firebase with the GCS image path
    set_firestore_document("image_urls", word, {"image_url": gcs_image_path})

    return gcs_image_path

async def generate_explanation(word: str) -> str:
    prompt = f"Explain the word '{word}' in a simple way that a 4-year-old child can understand."
    response = await chat_completion(prompt)
    return response.strip()

async def generate_story(word: str) -> str:
    prompt = f"Create a short and simple story for a 4-year-old child that includes the word '{word}'."
    response = await chat_completion(prompt)
    return response.strip()

async def generate_fact(word: str) -> str:
    prompt = f"Share an interesting and simple fact about the word '{word}' that a 4-year-old child would enjoy."
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
        image_url_future = get_image_url_from_firebase(word_data.word)
        explanation_future = generate_explanation(word_data.word)
        story_future = generate_story(word_data.word)
        fact_future = generate_fact(word_data.word)

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
