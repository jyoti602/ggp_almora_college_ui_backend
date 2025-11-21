from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    email: str
    message: str

    class Config:
        orm_mode = True
