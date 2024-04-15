# invalid_token.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class InvalidToken(Base):
    __tablename__ = "invalid_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="invalid_tokens")

    def __repr__(self):
        return f"<InvalidToken {self.token}>"

    def __str__(self):
        return self.token