from sqlalchemy import Column, Integer, String, Enum as SAEnum
from app.core.database import Base
from app.core.roles import Role

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(SAEnum(Role), nullable=False, default='user')
    hashed_password = Column(String, nullable=False)
