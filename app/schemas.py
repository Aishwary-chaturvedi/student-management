
from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    course: str
    year: int


class StudentUpdate(BaseModel):
    name: str
    email: str
    phone: str
    course: str
    year: int


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    course: str
    year: int

    model_config = ConfigDict(from_attributes=True)
