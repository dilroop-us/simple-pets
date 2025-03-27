from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from database import initialize_global_data
from routes import users, pets, favorites

app = FastAPI(
    title="Pet API",
    description="Pet Adoption & Listing API with FastAPI + Firebase",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pets.router, prefix="/pets", tags=["Pets"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])

# Optional: image uploads folder
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
def startup_event():
    initialize_global_data()

@app.get("/")
def root():
    return {"message": "Welcome to the Pet API!"}
