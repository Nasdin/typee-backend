from google.cloud import firestore
import openai

db = firestore.Client()



async def get_image_url_from_firebase(word: str) -> str:
    doc_ref = db.collection("image_urls").document(word)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()["image_url"]

    # If the image URL is not found in Firebase, get it from Google
    image_url = await get_image_from_google(word)

    # Upload the image to Google Cloud Storage
    gcs_image_path = await upload_image_to_gcs(image_url)

    # Update Firebase with the GCS image path
    doc_ref.set({"image_url": gcs_image_path})

    return gcs_image_path

async def generate_explanation(word: str) -> str:
    prompt = f"Explain the word '{word}' in a simple way that a 4-year-old child can understand."
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response['choices'][0]['message']['content'].strip()

async def generate_story(word: str) -> str:
    prompt = f"Create a short and simple story for a 4-year-old child that includes the word '{word}'."
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response['choices'][0]['message']['content'].strip()


async def generate_fact(word: str) -> str:
    prompt = f"Share an interesting and simple fact about the word '{word}' that a 4-year-old child would enjoy."
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response['choices'][0]['message']['content'].strip()


async def kid_word_encyclopedia(word_data: WordData):
    doc_ref = db.collection("word_data").document(word_data.word)
    doc = doc_ref.get()

    if doc.exists:
        # Data found in Firestore, return as WordInfo object
        word_info = WordInfo(**doc.to_dict())
    else:
        # Data not found in Firestore, generate with OpenAI API
        # Call OpenAI API to generate imageUrl, explanation, story, and fact
        image_url_future = get_image_url_from_firebase(word_data.word)
        explanation_future = generate_explanation(word_data.word)
        story_future = generate_story(word_data.word)
        fact_future = generate_fact(word_data.word)

        # Save generated data to Firestore
        data = {
            "imageUrl": image_url,
            "explanation": explanation,
            "story": story,
            "fact": fact,
        }
        doc_ref.set(data)

        # Create WordInfo object
        word_info = WordInfo(**data)

    return word_info