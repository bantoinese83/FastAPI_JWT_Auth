# profile.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profiles")
    full_name = Column(String)
    birth_date = Column(Date)
    avatar = Column(String)
    bio = Column(String)
    location = Column(String)
    website = Column(String)
    social = Column(String)

    def __repr__(self):
        return f"<Profile {self.full_name}>"

    def __str__(self):
        return self.full_name