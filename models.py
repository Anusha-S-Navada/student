from sqlalchemy import Integer, String, Column
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    grade = Column(Integer)
    age = Column(Integer)

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    qualification = Column(String)


