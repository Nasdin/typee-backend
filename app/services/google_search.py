import httpx
from google.cloud import storage, firestore
import uuid
import asyncio

from app.core.config import GCP_BUCKET_NAME, GOOGLE_API_KEY, GOOGLE_CSE_ID

# Set up Google Cloud Storage
storage_client = storage.Client()
bucket = storage_client.get_bucket(GCP_BUCKET_NAME)

# Set up Google Cloud Firestore
db = firestore.Client()


async def get_image_from_google(word: str) -> str:
    async with httpx.AsyncClient() as client:
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "searchType": "image",
            "q": word,
            "safe": "active",
        }
        response = await client.get(base_url, params=params)
    result = response.json()

    # Return the URL of the first image result
    return result["items"][0]["link"]


async def upload_image_to_gcs(image_url: str) -> str:
    # Download the image
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
    image_data = response.content

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.jpg"

    # Upload the image to Google Cloud Storage
    blob = bucket.blob(filename)
    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: blob.upload_from_string(image_data, content_type="image/jpeg"))

    # Return the GCS image path
    return f"gs://{GCP_BUCKET_NAME}/{filename}"


async def update_firebase_with_gcs_image_path(word: str, gcs_image_path: str):
    doc_ref = db.collection("image_urls").document(word)
    # Use a thread to run synchronous code
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: doc_ref.set({"image_url": gcs_image_path}))
