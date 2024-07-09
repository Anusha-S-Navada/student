import re
from typing import Optional, List
from pydantic import BaseModel,  EmailStr, validator
from models import Student, Teacher
from enum import Enum

class grade(BaseModel):
    id : int
    gradeName : str


class stud(BaseModel):
    id : int
    name : str
    grade_id : int
    age : int
    email : EmailStr

@validator('email')
def validate_email(cls, v):
    email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    if not email_pattern.match(v) or '..' in v or '@@' in v:
        raise ValueError('Invalid email format')
    return v
    

class stud_update(BaseModel):
    name: str = None
    grade_id: Optional[int] = None
    age: Optional[int] = None

    class Config:
        orm_mode = True

class teach(BaseModel):
    id : int
    name : str
    qualification : str
    grade_id : int
    email : EmailStr

class teach_update(BaseModel):
    name: str   
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


