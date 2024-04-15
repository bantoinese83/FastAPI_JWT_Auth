from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.crud import get_user_by_username, create_user
from app.db.database import get_db
from app.schemas.user_schemas import User, UserCreate
from app.services.auth_service import get_current_user
from app.utils.hash_password_utils import get_password_hash

router = APIRouter()


@router.post("/register", response_model=User, tags=["User"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return create_user(db=db, user=user)


@router.put("/users/me", response_model=User, tags=["User"])
def update_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update the current user's information.
    """
    current_user.email = user.email or current_user.email
    if user.hashed_password:
        current_user.hashed_password = get_password_hash(user.hashed_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/users/me", response_model=User, tags=["User"])
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete the current user's account.
    """
    db.delete(current_user)
    db.commit()
    return {"detail": "Account successfully deleted"}


@router.get("/users/me", response_model=User, tags=["User"])
def get_user(current_user: User = Depends(get_current_user)):
    """
    Get information about the current user.
    """
    return current_user


@router.delete("/users/me", response_model=User, tags=["User"])
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete the current user's account.
    """
    db.delete(current_user)
    db.commit()
    return {"detail": "Account successfully deleted"}

