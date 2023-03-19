import os
import requests
from google.cloud import storage
from google.cloud import firestore

# Set up Google Cloud Storage
storage_client = storage.Client()
bucket_name = os.environ["BUCKET_NAME"]
bucket = storage_client.get_bucket(bucket_name)

# Set up Google Cloud Firestore
db = firestore.Client()

# Google Custom Search API credentials
api_key = os.environ["GOOGLE_API_KEY"]
cx = os.environ["GOOGLE_CSE_ID"]

async def get_image_from_google(word: str) -> str:
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "searchType": "image",
        "q": word,
        "safe": "active",
    }
    response = requests.get(base_url, params=params)
    result = response.json()

    # Return the URL of the first image result
    return result["items"][0]["link"]

async def upload_image_to_gcs(image_url: str) -> str:
    # Download the image
    image_data = requests.get(image_url).content

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.jpg"

    # Upload the image to Google Cloud Storage
    blob = bucket.blob(filename)
    blob.upload_from_string(image_data, content_type="image/jpeg")

    # Return the GCS image path
    return f"gs://{bucket_name}/{filename}"

async def update_firebase_with_gcs_image_path(word: str, gcs_image_path: str):
    doc_ref = db.collection("image_urls").document(word)
    doc_ref.set({"image_url": gcs_image_path})