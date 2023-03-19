from google.cloud import storage
from config import GCP_BUCKET_NAME

storage_client = storage.Client()
bucket = storage_client.get_bucket(GCP_BUCKET_NAME)

def upload_blob(file_path: str, destination_blob_name: str):
    """Upload a file to GCS."""
    blob = bucket.blob(destination_blob_name)
    with open(file_path, "rb") as file:
        blob.upload_from_file(file)
    return blob.public_url

def download_blob(source_blob_name: str, destination_file_name: str):
    """Download a file from GCS."""
    blob = bucket.blob(source_blob_name)
    with open(destination_file_name, "wb") as file:
        blob.download_to_file(file)

def delete_blob(blob_name: str):
    """Delete a file from GCS."""
    blob = bucket.blob(blob_name)
    blob.delete()
