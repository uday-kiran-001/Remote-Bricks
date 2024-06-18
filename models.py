from pydantic import BaseModel, EmailStr

class UserRegistration(BaseModel):
    username: str   # Username of the user (string)
    email: EmailStr  # Email address of the user (validated as EmailStr)
    password: str    # Password of the user (string)

class UserLogin(BaseModel):
    email: EmailStr  # Email address of the user (validated as EmailStr)
    password: str    # Password of the user (string)

class LinkID(BaseModel):
    username: str    # Username of the user (string)
    linked_id: str   # ID to be linked to the user's account (string)
