from typing import Optional
from pydantic import BaseModel

class stud(BaseModel):
    id : int
    name : str
    grade : int
    age : int
    
class stud_update(BaseModel):
    name: Optional[str] = None
    grade: Optional[int] = None
    age: Optional[int] = None

