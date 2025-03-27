from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Users
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

# Pets
class ContactDetails(BaseModel):
    name: str
    phoneNumber: str
    email: str
    image: Optional[str]

class PetCreate(BaseModel):
    petName: str
    type: str
    breed: str
    age: int
    weight: str
    gender: str
    description: str
    health_status: bool
    vaccination_status: bool
    breeding_first_time: bool
    pedigree_certified: bool
    size: str
    friendly_with_other_pets: bool
    good_with_kids: bool
    is_trained: bool
    special_needs: List[str]
    image_urls: List[str]
    location: str
    available_for_adoption: bool
    contact_details: ContactDetails
