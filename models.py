from sqlalchemy import Integer, String, Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    grade_id = Column(Integer, ForeignKey('grades.id'))
    age = Column(Integer)
    
    grade = relationship("Grade", back_populates="students")


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    qualification = Column(String)
    grade_id = Column(Integer, ForeignKey('grades.id'))

    grade = relationship("Grade", back_populates="teachers")

   

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key = True, index = True)
    gradeName = Column(String, index = True)

    students = relationship("Student", back_populates="grade")
    teachers = relationship("Teacher", back_populates="grade")

