from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Contact
from schemas import ContactCreate

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contact")
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    new_contact = Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"message": "Contact saved successfully", "data": new_contact}
