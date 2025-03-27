from fastapi import APIRouter, Depends, HTTPException
from database import db
from datetime import datetime
from core.auth import get_current_user
import uuid

router = APIRouter()

@router.post("/{pet_id}")
def add_to_favorites(pet_id: str, user_id: str = Depends(get_current_user)):
    fav_id = str(uuid.uuid4())
    fav_ref = db.collection("users").document(user_id).collection("favorites").document(fav_id)
    fav_data = {
        "pet_id": pet_id,
        "created_at": datetime.utcnow().isoformat()
    }
    fav_ref.set(fav_data)
    return {"message": "Added to favorites", "favorite_id": fav_id}

@router.get("/")
def list_favorites(user_id: str = Depends(get_current_user)):
    fav_docs = db.collection("users").document(user_id).collection("favorites").stream()
    result = []
    for fav in fav_docs:
        fav_data = fav.to_dict()
        pet_doc = db.collection("pets").document(fav_data["pet_id"]).get()
        if pet_doc.exists:
            result.append({
                "favorite_id": fav.id,
                "pet": pet_doc.to_dict()
            })
    return result

@router.delete("/{favorite_id}")
def remove_favorite(favorite_id: str, user_id: str = Depends(get_current_user)):
    fav_ref = db.collection("users").document(user_id).collection("favorites").document(favorite_id)
    if not fav_ref.get().exists:
        raise HTTPException(status_code=404, detail="Favorite not found")
    fav_ref.delete()
    return {"message": "Favorite removed"}
