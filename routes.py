from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import List
from models import UserRegistration, UserLogin, LinkID
from utils import get_password_hash, verify_password

router = APIRouter()

# Registration API
@router.post("/register", response_description="Register a new user", status_code=status.HTTP_201_CREATED)
def register_user(request: Request, user: UserRegistration = Body(...)):
    user = jsonable_encoder(user)
    users_collection = request.app.database["users"]
    
    # Check if email is already registered
    if users_collection.find_one({"email": user["email"]}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is already registered
    if users_collection.find_one({"username": user["username"]}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password before storing
    user["password"] = get_password_hash(user["password"])
    new_user = users_collection.insert_one(user)
    created_user = users_collection.find_one({"_id": new_user.inserted_id})
    
    return {"user_id": str(created_user["_id"]), "username": created_user["username"]}

# Login API
@router.post("/login", response_description="User login", status_code=status.HTTP_200_OK)
def login_user(request: Request, user: UserLogin = Body(...)):
    users_collection = request.app.database["users"]
    db_user = users_collection.find_one({"email": user.email})
    
    # Validate credentials
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"user_id": str(db_user["_id"]), "username": db_user["username"]}

# Linking ID API
@router.post("/link_id", response_description="Link an ID to a user's account", status_code=status.HTTP_200_OK)
def link_id(request: Request, link: LinkID = Body(...)):
    users_collection = request.app.database["users"]
    linked_ids_collection = request.app.database["linked_ids"]
    
    # Check if the user exists
    user = users_collection.find_one({"username": link.username})
    if not user:
        raise HTTPException(status_code=400, detail="User not Registered")
    
    # Insert the linked ID
    linked_ids_collection.insert_one({"username": link.username, "linked_id": link.linked_id})
    return {"message": "ID linked successfully"}

# Join API
@router.get("/user_with_ids/{username}", response_description="Get user with linked IDs", status_code=status.HTTP_200_OK)
def get_user_with_ids(username: str, request: Request):
    users_collection = request.app.database["users"]
    linked_ids_collection = request.app.database["linked_ids"]
    
    # Check if the user exists
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Retrieve linked IDs
    linked_ids = linked_ids_collection.find({"username": username})
    linked_ids_list = [linked_id["linked_id"] for linked_id in linked_ids]
    
    return {"message": "Successfull"}

# Delete API
@router.delete("/delete_user/{username}", response_description="Delete user and all associated data", status_code=status.HTTP_200_OK)
def delete_user(username: str, request: Request):
    users_collection = request.app.database["users"]
    linked_ids_collection = request.app.database["linked_ids"]
    
    # Check if the user exists
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Delete user and associated linked IDs
    users_collection.delete_one({"username": username})
    linked_ids_collection.delete_many({"username": username})
    
    return {"message": "User and all associated data deleted successfully"}
