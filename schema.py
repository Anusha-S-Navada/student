from typing import Optional
from pydantic import BaseModel

class grade(BaseModel):
    id : int
    gradeName : str

class stud(BaseModel):
    id : int
    name : str
    grade_id : int
    age : int

class StudentWithTeacher(BaseModel):
    student_name : str
    gradename : str
    teacher_name : str
    teacher_qualification : str
    
class stud_update(BaseModel):
    name: Optional[str] = None
    grade: Optional[int] = None
    age: Optional[int] = None

class teach(BaseModel):
    id : int
    name : str
    qualification : str
    grade_id : int

class teach_update(BaseModel):
    name: Optional[str] = None  
    qualification : Optional[str] 
    grade_id : Optional[int]