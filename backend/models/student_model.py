from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_no = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    mobile = Column(String(20), nullable=False)
    year = Column(String(20), nullable=False)  # e.g. '1st Year'
    branch = Column(String(100), nullable=False)
