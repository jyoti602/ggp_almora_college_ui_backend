from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal, Base
from models.user import User
from passlib.context import CryptContext
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password"
        )


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to create user with email: {user.email}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password
        hashed_password = hash_password(user.password)
        logger.info("Password hashed successfully")
        
        # Create new user
        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created successfully with ID: {db_user.id}")
        print(db_user)
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )