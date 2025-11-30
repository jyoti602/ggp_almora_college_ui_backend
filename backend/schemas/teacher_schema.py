from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    department: str
    mobile: str

    class Config:
        orm_mode = True


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    mobile: str | None = None

    class Config:
        orm_mode = True
