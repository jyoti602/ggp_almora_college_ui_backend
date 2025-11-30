from sqlalchemy import Column, Integer, String
from database import Base


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False)
