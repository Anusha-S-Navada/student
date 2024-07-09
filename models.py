from sqlalchemy import DateTime, Enum, Integer, String, Column,ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship

student_teacher = Table(
    'student_teacher',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('teacher_id', Integer, ForeignKey('teachers.id'))
)



class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    grade_id = Column(Integer, ForeignKey('grades.id'))
    age = Column(Integer)
    email = Column(String, unique=True)
    
    grade = relationship("Grade", back_populates="students")
    teachers = relationship("Teacher", secondary=student_teacher, back_populates="students")



class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    qualification = Column(String)
    grade_id = Column(Integer, ForeignKey('grades.id'))
    email = Column(String, unique=True)

    grade = relationship("Grade", back_populates="teachers")
    students = relationship("Student", secondary=student_teacher, back_populates="teachers")

   

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key = True, index = True)
    gradeName = Column(String, index = True)

    students = relationship("Student", back_populates="grade")
    teachers = relationship("Teacher", back_populates="grade")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    recipient_type = Column(Enum('student', 'teacher', name='recipient_types'), nullable=False)
    recipient_id = Column(Integer, nullable=False)
    event_type = Column(Enum('holiday', 'exam', 'event', name='event_types'), nullable=True)
    event_details = Column(String, nullable=True)

