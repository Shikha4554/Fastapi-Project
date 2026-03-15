from pydantic import BaseModel, EmailStr, Field
from pydantic.functional_validators import field_validator
from datetime import datetime
import re

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=3, max_length=50)

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can contain only letters, numbers, and underscore")
        return v


    @field_validator("full_name")
    @classmethod
    def full_name_valid(cls, v):
        if not re.match(r"^[a-zA-Z ]+$", v):
            raise ValueError("Full name must contain only letters and spaces")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# CRUD MODELS#

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)

    @field_validator("title")
    @classmethod
    def title_valid(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or just spaces")
        if not re.match(r"^[a-zA-Z0-9 ,.?!-]+$", v):
            raise ValueError("Title contains invalid characters")
        return v

    @field_validator("description")
    @classmethod
    def description_valid(cls, v):
        if not v.strip():
            raise ValueError("Description cannot be empty or just spaces")
        return v

# class Todo(BaseModel):
#     user_id:str
#     title:str|None
#     description:str|None
#     completed:bool|None
#     created_at: datetime



#     class CollectionName:
#         todo="todo"

class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
    completed: bool = Field(..., description="Task completion status (True or False)")

    @field_validator("title")
    @classmethod
    def title_valid(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or just spaces")
        if not re.match(r"^[a-zA-Z0-9 ,.?!-]+$", v):
            raise ValueError("Title contains invalid characters")
        return v

    @field_validator("description")
    @classmethod
    def description_valid(cls, v):
        if not v.strip():
            raise ValueError("Description cannot be empty or just spaces")
        return v

    @field_validator("completed")
    @classmethod
    def completed_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError("Completed must be a boolean value (True or False)")
        return v


class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
