import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
if not FIREBASE_CREDENTIALS:
    raise ValueError("FIREBASE_CREDENTIALS env variable missing!")

try:
    FIREBASE_CREDENTIALS_DICT = json.loads(base64.b64decode(FIREBASE_CREDENTIALS).decode())
except Exception as e:
    raise ValueError(f"Failed to decode FIREBASE_CREDENTIALS: {e}")
