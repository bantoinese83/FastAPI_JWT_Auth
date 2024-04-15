from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud import get_profile_by_user_id, update_profile, delete_profile
from app.db.database import get_db
from app.schemas.user_schemas import User, ProfileCreate, Profile
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/users/me/profile", response_model=Profile, tags=["Profile"])
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get the current user's profile.
    """
    profile = get_profile_by_user_id(db, user_id=current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/users/me/profile", response_model=Profile, tags=["Profile"])
def update_user_profile(profile: ProfileCreate, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Update the current user's profile.
    """
    updated_profile = update_profile(db=db, profile=profile, user_id=current_user.id)
    return updated_profile


@router.delete("/users/me/profile", tags=["Profile"])
def delete_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete the current user's profile.
    """
    delete_profile(db, user_id=current_user.id)
    return {"detail": "Profile successfully deleted"}
