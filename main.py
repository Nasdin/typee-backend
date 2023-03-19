# This file initializes and starts the FastAPI application which creates the backend for Typee the robot.

from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore
import openai

# Initialize Firebase
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"

app = FastAPI()

class WordData(BaseModel):
    word: str

@app.post("/is-word-safe")
async def is_word_safe(word_data: WordData):
    word = word_data.word

    # Call OpenAI API to check if the word is safe
    # Implement your logic here

    return {"safe": True}  # Change this based on your logic

@app.post("/kid-word-encyclopedia")
async def kid_word_encyclopedia(word_data: WordData):
    word = word_data.word

    # Check if data exists in Firebase
    doc_ref = db.collection("words").document(word)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()

    # If not, generate data using OpenAI API and store it in Firebase
    # Implement your logic here (similar to getWordData in wordsApi.js)

    data = {
        "imageUrl": "image_url_here",
        "explanation": "explanation_here",
        "story": "story_here",
        "fact": "fact_here",
    }

    doc_ref.set(data)

    return data