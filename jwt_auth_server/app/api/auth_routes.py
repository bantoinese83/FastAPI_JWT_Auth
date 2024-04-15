from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth_schemas import Token
from app.schemas.user_schemas import User
from app.services.auth_service import (
    get_current_user,
    authenticate_user,
    create_access_token,
    oauth2_scheme,
    logout_user,
    refresh_user_token
)

router = APIRouter()


@router.post("/login", response_model=Token, tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in and obtain an access token.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", tags=["Authentication"])
def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme),
           db: Session = Depends(get_db)):
    """
    Log out the current user.
    """
    logout_user(db, current_user, token)
    return {"detail": "Logout successful"}


@router.post("/refresh-token", response_model=Token, tags=["Authentication"])
def refresh_token(jwt_refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh an expired access token using a refresh token.
    """
    return refresh_user_token(db, jwt_refresh_token)
