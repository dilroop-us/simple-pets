import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

firebase_credentials_str = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_credentials_str:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is missing!")

try:
    firebase_credentials_json = base64.b64decode(firebase_credentials_str).decode()
    FIREBASE_CREDENTIALS = json.loads(firebase_credentials_json)
except Exception as e:
    raise ValueError(f"Failed to decode FIREBASE_CREDENTIALS: {e}")

cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db = firestore.client()

def initialize_global_data():
    print("🔥 Firebase initialized and ready!")
