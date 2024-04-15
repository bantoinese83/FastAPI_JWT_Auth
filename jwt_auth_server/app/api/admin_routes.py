from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.crud import get_users, create_user
from app.db.database import get_db
from app.schemas.user_schemas import User, UserCreate
from app.services.auth_service import get_current_admin_user
from app.utils.hash_password_utils import get_password_hash
from app.crud.crud import get_user_by_username

router = APIRouter()



@router.post("/register-admin", response_model=User, tags=["Admin"])
def register_admin(user: UserCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_admin_user)):
    """
    Register a new admin user.
    """
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return create_user(db=db, user=user, is_admin=True)


@router.get("/users/{username}", response_model=User, tags=["Admin"])
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get a user by username.
    """
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/admin/users", response_model=List[User], tags=["Admin"])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """
    Get all users (admin only).
    """
    users = get_users(db)
    return users


@router.put("/admin/users/{username}", response_model=User, tags=["Admin"])
def admin_update_user(username: str, user: UserCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_admin_user)):
    """
    Update a user (admin only).
    """
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email or db_user.email
    if user.hashed_password:
        db_user.hashed_password = get_password_hash(user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/admin/users/{username}", tags=["Admin"])
def admin_delete_user(username: str, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_admin_user)):
    """
    Delete a user (admin only).
    """
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User successfully deleted"}
