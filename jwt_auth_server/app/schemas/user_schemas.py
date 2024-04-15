from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    disabled: Optional[bool] = False

class UserCreate(UserBase):
    username: str
    hashed_password: str
    is_admin: Optional[bool] = None



class User(UserBase):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    social: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True