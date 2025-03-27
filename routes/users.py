from fastapi import APIRouter, Depends, HTTPException
from schemas import UserRegister, UserLogin, UserUpdate
from database import db
from core.auth import create_access_token, hash_password, verify_password, get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/register")
def register_user(user: UserRegister):
    existing = db.collection("users").where("email", "==", user.email).get()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    doc_ref = db.collection("users").document()
    user_data = {
        "id": doc_ref.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "password": hashed_pw,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    doc_ref.set(user_data)
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.post("/login")
def login(user: UserLogin):
    users = db.collection("users").where("email", "==", user.email).get()
    if not users:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_data = users[0].to_dict()

    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.put("/profile")
def update_profile(user_update: UserUpdate, email: str = Depends(get_current_user)):
    user_query = db.collection("users").where("email", "==", email).get()
    if not user_query:
        raise HTTPException(status_code=404, detail="User not found")

    user_doc = user_query[0]
    user_ref = db.collection("users").document(user_doc.id)
    updates = {k: v for k, v in user_update.dict().items() if v is not None}
    updates["updated_at"] = datetime.utcnow().isoformat()
    user_ref.update(updates)
    return {"message": "Profile updated"}
