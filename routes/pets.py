from fastapi import APIRouter, Depends, HTTPException
from database import db
from core.auth import get_current_user
from schemas import PetCreate
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/")
def create_pet(pet: PetCreate, user_id: str = Depends(get_current_user)):
    pet_id = str(uuid.uuid4())
    pet_data = pet.dict()
    pet_data.update({
        "id": pet_id,
        "owner_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    db.collection("pets").document(pet_id).set(pet_data)
    return {"message": "Pet added", "pet_id": pet_id}

@router.get("/")
def list_all_pets():
    pets = db.collection("pets").stream()
    return [doc.to_dict() for doc in pets]

@router.get("/{pet_id}")
def get_pet(pet_id: str):
    pet_doc = db.collection("pets").document(pet_id).get()
    if not pet_doc.exists:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet_doc.to_dict()

@router.put("/{pet_id}")
def update_pet(pet_id: str, pet: PetCreate, user_id: str = Depends(get_current_user)):
    pet_ref = db.collection("pets").document(pet_id)
    pet_doc = pet_ref.get()
    if not pet_doc.exists:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet_doc.to_dict()["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_data = pet.dict()
    updated_data["updated_at"] = datetime.utcnow().isoformat()
    pet_ref.update(updated_data)
    return {"message": "Pet updated"}

@router.delete("/{pet_id}")
def delete_pet(pet_id: str, user_id: str = Depends(get_current_user)):
    pet_ref = db.collection("pets").document(pet_id)
    pet_doc = pet_ref.get()
    if not pet_doc.exists:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet_doc.to_dict()["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    pet_ref.delete()
    return {"message": "Pet deleted"}
