#  This folder contains the main FastAPI application and its components.from fastapi import FastAPI
from .api import router
import firebase_admin
from firebase_admin import auth


app = FastAPI()
firebase_admin.initialize_app()

app.include_router(router)
