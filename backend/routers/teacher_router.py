from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models.teacher_model import Teacher
from schemas.teacher_schema import TeacherBase, TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[TeacherBase])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()


@router.post("/", response_model=TeacherBase, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(Teacher).filter(Teacher.email == teacher.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher with this email already exists",
        )

    new_teacher = Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


@router.put("/{teacher_id}", response_model=TeacherBase)
def update_teacher(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    db.delete(teacher)
    db.commit()
    return None


@router.get("/count")
def get_teachers_count(db: Session = Depends(get_db)):
    total_teachers = db.query(Teacher).count()
    
    return {
        "totalTeachers": total_teachers,
    }
