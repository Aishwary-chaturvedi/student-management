
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate, StudentResponse

app = FastAPI(title="Student Management System")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management System"
    }


# Get all students
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# Register a new student
@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    email = student.email.strip().lower()

    existing_student = db.query(Student).filter(
        Student.email == email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_student = Student(
        name=student.name.strip().title(),
        email=email,
        phone=student.phone.strip(),
        course=student.course.strip(),
        year=student.year
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# Get student by ID
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# Update student
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_email = updated_data.email.strip().lower()

    existing_student = db.query(Student).filter(
        Student.email == new_email,
        Student.id != student_id
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    student.name = updated_data.name.strip().title()
    student.email = new_email
    student.phone = updated_data.phone.strip()
    student.course = updated_data.course.strip()
    student.year = updated_data.year

    db.commit()
    db.refresh(student)

    return student
