from sqlalchemy.orm import Session
from app.schemas import user_schemas
from app.utils.hash_password_utils import get_password_hash
from app.models.user import User
from app.models.profile import Profile as ProfileModel
from app.schemas.user_schemas import ProfileCreate
from fastapi import HTTPException


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schemas.UserCreate, is_admin: bool = False):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(ProfileModel).filter(ProfileModel.user_id == user_id).first()


def update_profile(db: Session, profile: ProfileCreate, user_id: int):
    db_profile = get_profile_by_user_id(db, user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, user_id: int):
    db_profile = get_profile_by_user_id(db, user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
