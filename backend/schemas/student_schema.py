from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    id: int | None = None
    name: str
    roll_no: str
    email: EmailStr
    mobile: str
    year: str
    branch: str

    class Config:
        orm_mode = True


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    roll_no: str | None = None
    email: EmailStr | None = None
    mobile: str | None = None
    year: str | None = None
    branch: str | None = None

    class Config:
        orm_mode = True
