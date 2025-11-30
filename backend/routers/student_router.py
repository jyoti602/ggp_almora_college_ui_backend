from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models.student_model import Student
from schemas.student_schema import StudentBase, StudentCreate, StudentUpdate

router = APIRouter(prefix="/api/students", tags=["Students"])


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[StudentBase])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/", response_model=StudentBase, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check duplicate roll_no or email
    existing = (
        db.query(Student)
        .filter(
            (Student.roll_no == student.roll_no) | (Student.email == student.email)
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this roll number or email already exists",
        )

    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.put("/{student_id}", response_model=StudentBase)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    db.delete(student)
    db.commit()
    return None


@router.get("/count")
def get_students_count(db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    first_year = db.query(Student).filter(Student.year == "1st Year").count()
    second_year = db.query(Student).filter(Student.year == "2nd Year").count()
    third_year = db.query(Student).filter(Student.year == "3rd Year").count()
    
    return {
        "totalStudents": total_students,
        "firstYearStudents": first_year,
        "secondYearStudents": second_year,
        "thirdYearStudents": third_year,
    }
