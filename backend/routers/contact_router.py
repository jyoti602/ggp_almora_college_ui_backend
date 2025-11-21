from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.contact_model import Contact
from backend.schemas.contact_schema import ContactBase

router = APIRouter(prefix="/api/contact", tags=["Contact"])

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_contact(contact: ContactBase, db: Session = Depends(get_db)):
    """Save contact form data to MySQL"""
    new_contact = Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"message": "Message sent successfully!"}
