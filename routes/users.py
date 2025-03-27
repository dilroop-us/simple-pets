from fastapi import APIRouter, Depends, HTTPException
from schemas import UserRegister, UserLogin, UserProfileUpdate
from database import db
from core.auth import create_access_token, hash_password, verify_password, get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/register")
def register_user(user: UserRegister):
    users_ref = db.collection("users").where("email", "==", user.email).stream()
    for doc in users_ref:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    doc_ref = db.collection("users").document()

    user_data = {
        "id": doc_ref.id,
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    doc_ref.set(user_data)

    # Create blank profile
    db.collection("profiles").document(doc_ref.id).set({
        "user_id": doc_ref.id,
        "name": "",
        "phone": None,
        "image": None
    })

    token = create_access_token({"sub": user.email})
    return {"access_token": token}


@router.post("/login")
def login(user: UserLogin):
    users = db.collection("users").where(filter=("email", "==", user.email)).get()
    if not users:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_data = users[0].to_dict()

    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}


@router.get("/profile")
def get_profile(email: str = Depends(get_current_user)):
    users = db.collection("users").where(filter=("email", "==", email)).get()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = users[0].id
    profile_doc = db.collection("profiles").document(user_id).get()
    if not profile_doc.exists:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile_doc.to_dict()


@router.put("/profile")
def update_profile(profile: UserProfileUpdate, email: str = Depends(get_current_user)):
    users = db.collection("users").where(filter=("email", "==", email)).get()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = users[0].id
    profile_ref = db.collection("profiles").document(user_id)

    update_data = {k: v for k, v in profile.dict().items() if v is not None}
    profile_ref.update(update_data)

    return {"message": "Profile updated"}
