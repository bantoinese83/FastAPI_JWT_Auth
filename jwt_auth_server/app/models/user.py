# user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.profile import Profile


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    remember_me = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    profiles = relationship(Profile, back_populates="user")
    invalid_tokens = relationship("InvalidToken", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return self.username