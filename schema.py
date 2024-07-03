from typing import Optional, List
from pydantic import BaseModel
from models import Student, Teacher

class grade(BaseModel):
    id : int
    gradeName : str


class stud(BaseModel):
    id : int
    name : str
    grade_id : int
    age : int
    

class stud_update(BaseModel):
    name: Optional[str] = None
    grade_id: Optional[int] = None
    age: Optional[int] = None

    class Config:
        orm_mode = True


class teach(BaseModel):
    id : int
    name : str
    qualification : str
    grade_id : int


class teach_update(BaseModel):
    name: Optional[str] = None  
    qualification : Optional[str] 
    grade_id : Optional[int]

    class Config:
        orm_mode = True


class StudentInfo(BaseModel):
    id: int
    name: str
    age: int
    grade_id: int


class TeacherInfo(BaseModel):
    id: int
    name: str
    qualification: str
    grade_id: int


class NotificationBase(BaseModel):
    id : int
    content: str
    recipient_type: str
    recipient_id: int
    event_type: Optional[str]
    event_details: Optional[str]

class NotificationRequest(BaseModel):
    content: str
    event_type: str
    event_details: str