import re
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models, schema, validation
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()
models.Base.metadata.create_all(bind= engine)


#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Grade module
@app.post("/grades/", tags=["Grade"])
def create_grade(grade : schema.grade, db: Session = Depends(get_db)):

    #checking grade_id is already existed or not
    existing_grade_id = db.query(models.Grade).filter(models.Grade.id == grade.id).first()
    if existing_grade_id:
        raise HTTPException(status_code=400, detail="Grade ID already exists")

    #Check if the grade name already exists
    existing_grade_name = db.query(models.Grade).filter(models.Grade.gradeName == grade.gradeName).first()
    if existing_grade_name:
        raise HTTPException(status_code=400, detail="Grade name already exists")
    
    new_grade = models.Grade(id = grade.id , gradeName=grade.gradeName)
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade


@app.delete('/del_grade/{id}', tags=["Grade"])
def delete_grade(id:int, db:Session = Depends(get_db)):
    deleted_grade = db.query(models.Grade).filter(models.Grade.id == id).first()
    if deleted_grade is None:
         raise HTTPException(status_code=404, detail="Grade not found")
    
    db.delete(deleted_grade)
    db.commit()
    return {f'grade of id:{id} deleted successfully'}


#CRUD operations on Student module

@app.post("/students/", response_model=schema.stud, tags=["Students"])
def create_student(stud : schema.stud, db: Session = Depends(get_db)):
    
    #student id should be unique
    existing_student = db.query(models.Student).filter(models.Student.id == stud.id).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists and must be unique")
    
    #student id should be positive and integer
    if not isinstance(stud.id, int) or stud.id <= 0:
        raise HTTPException(status_code=400, detail="Student ID should be a positive integer")

    #checks if name is more than 3 words
    if len(stud.name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
    
    #checks if name is string 
    if not stud.name.isalpha():
        raise HTTPException(status_code=400, detail="Name can only contain alphabetic characters")
    
    #Checks if the grade ID existed or not
    existing_grade = db.query(models.Grade).filter(models.Grade.id == stud.grade_id).first()
    if not existing_grade:
        raise HTTPException(status_code=400, detail="Grade ID not found")

    #grade id must be provided
    if not stud.grade_id:
        raise HTTPException(status_code=400, detail="Grade ID is required")
    
    #checks if the age is more than 5
    if not isinstance(stud.age, int) or stud.age < 6:
        raise HTTPException(status_code=400, detail="Age should be more than 5 years")
   
    stud.name = stud.name.capitalize()
    new_student = models.Student(**stud.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get('/allstudents/', tags=["Students"])
def get_student(db: Session = Depends(get_db)):
    student_info = db.query(models.Student).all()
    return {"Student information": student_info}


@app.get('/students/{id}', tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    student_info = db.query(models.Student).filter(models.Student.id == id).first()
    if student_info is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"Student information": student_info}


#Pagination
@app.get("/students/",tags=["Students"])
async def get_students(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Skip and Limit must be positive integers")
    return db.query(models.Student).offset(skip).limit(limit).all()


@app.put('/stud/{id}', tags=["Students"])
def update_student(id: int, stud: schema.stud_update, db: Session = Depends(get_db)):
    #check student id is existed or not
    updated_stud = db.query(models.Student).filter(models.Student.id == id).first()
    if updated_stud is None:
        raise HTTPException(status_code=404, detail="Student not found")

    #check if all required fields are provided
    if not (stud.name and stud.grade_id and stud.age):
        raise HTTPException(status_code=400, detail="Name, grade_id, and age must be provided")
    
    #checks length of student name
    if len(stud.name.strip()) < 3:
        raise HTTPException(status_code=400,detail="Name should be atleast 3 letters")
    
    #checks name is string or not
    if not stud.name.isalpha():
        raise HTTPException(status_code=400, detail="Name can only contain alphabetic characters")

    #Checks if the grade ID existed or not
    existing_grade = db.query(models.Grade).filter(models.Grade.id == stud.grade_id).first()
    if not existing_grade:
        raise HTTPException(status_code=400, detail="Grade ID not found")

    
    if stud.name is not None:
        updated_stud.name = stud.name.capitalize()
    if stud.grade_id is not None:
        updated_stud.grade_id = stud.grade_id
    if stud.age is not None:
        updated_stud.age = stud.age
    db.commit()
    db.refresh(updated_stud)
    return {"message": "Student updated successfully", "Student information": updated_stud}


@app.delete('/del_stud/{id}', tags=["Students"])
def delete_student(id:int, db:Session = Depends(get_db)):
    deleted_student = db.query(models.Student).filter(models.Student.id == id).first()
    if deleted_student is None:
         raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(deleted_student)
    db.commit()
    return {f'student of id:{id} deleted successfully'}


#CRUD operations on Teachers module
@app.post("/teachers/", response_model=schema.teach, tags=["Teachers"])
def create_teacher(teaching : schema.teach, db: Session = Depends(get_db)):
    #checks if name is more than 3 words
    if len(teaching.name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
    
    #checks if name is string 
    if not teaching.name.isalpha():
        raise HTTPException(status_code=400, detail="Name can only contain alphabetic characters")
    
    #checks if teachers id is unique
    existing_teacher = db.query(models.Teacher).filter(models.Teacher.id == teaching.id).first()
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher ID already exists and must be unique")
    
    #teachers id should be positive and integer
    if not isinstance(teaching.id, int) or teaching.id <= 0:
        raise HTTPException(status_code=400, detail="Teacher ID should be a positive integer")
    
    #grade id must be provided
    if not teaching.grade_id:
        raise HTTPException(status_code=400, detail="Grade ID is required")
    
    #Checks if the grade ID existed or not
    existing_grade = db.query(models.Grade).filter(models.Grade.id == teaching.grade_id).first()
    if not existing_grade:
        raise HTTPException(status_code=400, detail="Grade ID not found")
    
    # Validate qualification (case-insensitive)
    valid_qualifications = {
        "bsc b.ed": "BSc B.ed",
        "msc m.ed": "MSc M.ed",
        "bsc": "BSc",
        "msc": "MSc"
    }
    qualification_lower = teaching.qualification.lower()
    if qualification_lower not in valid_qualifications:
        raise HTTPException(status_code=400, detail="Invalid Qualification, qualification should be 'BSc', 'MSc', 'BSc B.ed' or 'MSc M.ed'")
    
    teaching.name = teaching.name.capitalize()
    teaching.qualification = valid_qualifications[qualification_lower]
    new_teacher = models.Teacher(**teaching.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    print(new_teacher)
    return new_teacher


@app.get('/allteachers/', tags=["Teachers"])
def get_teacher(db: Session = Depends(get_db)):
    teacher_info = db.query(models.Teacher).all()
    return {"Teacher information": teacher_info}


@app.get('/teachers/{id}', tags=["Teachers"])
def get_teacher(id: int, db: Session = Depends(get_db)):
    teacher_info = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if teacher_info is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"Teacher information": teacher_info}

@app.put('/teach/{id}', tags=["Teachers"])
def update_teach(id: int, teach: Optional[schema.teach_update] = None, db: Session = Depends(get_db)):

    updated_teach = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not updated_teach:
        raise HTTPException(status_code=400, detail="Teacher ID not found")
    
    #check if all required fields are provided
    if not (teach.name and teach.grade_id and teach.qualification):
        raise HTTPException(status_code=400, detail="Name, grade_id, and age must be provided")
    
    #checks if name is more than 3 words
    if len(teach.name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
    
    #checks if name is string 
    if not teach.name.isalpha():
        raise HTTPException(status_code=400, detail="Name can only contain alphabetic characters")

    # Validate qualification (case-insensitive)
    valid_qualifications = {
        "bsc b.ed": "BSc B.ed",
        "msc m.ed": "MSc M.ed",
        "bsc": "BSc",
        "msc": "MSc"
    }
    qualification_lower = teach.qualification.lower()
    if qualification_lower not in valid_qualifications:
        raise HTTPException(status_code=400, detail="Invalid Qualification, qualification should be 'BSc', 'MSc', 'BSc B.ed' or 'MSc M.ed'")
    
    #Checks if the grade ID existed or not
    existing_grade = db.query(models.Grade).filter(models.Grade.id == teach.grade_id).first()
    if not existing_grade:
        raise HTTPException(status_code=400, detail="Grade ID not found")
    

    if teach.name is not None:
        updated_teach.name = teach.name.capitalize()
    if teach.qualification is not None:
        updated_teach.qualification = teach.qualification
    if teach.grade_id is not None:
        updated_teach.grade_id = teach.grade_id
    db.commit()
    db.refresh(updated_teach)
    return {"message": "Teacher updated successfully", "Teacher information": updated_teach} 


@app.delete('/del_teach/{id}', tags=["Teachers"])
def delete_teacher(id:int, db:Session = Depends(get_db)):
    deleted_teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if deleted_teacher is None:
         raise HTTPException(status_code=404, detail="Teacher not found")
    
    db.delete(deleted_teacher)
    db.commit()
    return {f'Teacher of id:{id} deleted successfully'}


#getting students information using grade id
@app.get("/students_by_grade/{grade_id}",tags=["retrieve"])
def get_students_by_grade(grade_id: int, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.grade_id == grade_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for the specified grade")
    return students


#getting teachers information using grade id
@app.get("/teachers_by_grade/{grade_id}",tags=["retrieve"])
def get_teachers_by_grade(grade_id: int, db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).filter(models.Teacher.grade_id == grade_id).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="No teacher found for the specified grade")
    return teachers


#getting students and teachers information using grade id             
@app.get("/student_with_teacher/{grade_id}", response_model=dict,tags=["retrieve"])
def get_grade_info(grade_id: int, db: Session = Depends(get_db)):
    grade_info = {}

    #grade
    grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    grade_info["grade_id"] = grade.id
    grade_info["grade_name"] = grade.gradeName

    #students information in this grade
    students = db.query(models.Student).filter(models.Student.grade_id == grade_id).all()
    if students:
        grade_info["students"] = [schema.StudentInfo(id=student.id, name=student.name, age=student.age, grade_id=student.grade_id) for student in students]
    else:
        grade_info["students"] = []
  
    #teachers information in this grade
    teachers = db.query(models.Teacher).filter(models.Teacher.grade_id == grade_id).all()
    if teachers:
        grade_info["teachers"] = [schema.TeacherInfo(id=teacher.id, name=teacher.name, qualification=teacher.qualification, grade_id=teacher.grade_id) for teacher in teachers]
    else:
        grade_info["teachers"] = []

    return grade_info


#counting total number of students in particular grade
@app.get('/count_students/{grade_id}', tags=["Count"])
def count_students(grade_id: int, db: Session = Depends(get_db)):
    count = db.query(models.Student).filter(models.Student.grade_id == grade_id).count()
    return {"grade_id": grade_id, "Total_student_count": count}


#counting total number of tudents in particular grade
@app.get('/count_teachers/{grade_id}',tags=["Count"])
def count_teachers(grade_id: int, db: Session = Depends(get_db)):
    count = db.query(models.Teacher).filter(models.Teacher.grade_id == grade_id).count()
    return {"grade_id": grade_id,"Total_teachers_count": count}

#Notification module
def send_notification(id: int, content: str, recipient_type: str, recipient_id: int, event_type: Optional[str] = None, event_details: Optional[str] = None, db: Session = None):
    notification = models.Notification(
        id=id,
        content=content,
        recipient_type=recipient_type,
        recipient_id=recipient_id,
        event_type=event_type,
        event_details=event_details
    )
    db.add(notification)
    db.commit()

#sending event notifications for one particular student/teacher
@app.post('/send_event_notification', tags=["Notifications"])
def send_event_notification(id:int,content: str, recipient_type: str, recipient_id: int, event_type: str, event_details: str, db: Session = Depends(get_db)):
    if recipient_type not in ['student', 'teacher']:
        raise HTTPException(status_code=400, detail="Recipient type must be 'student' or 'teacher'")
    
    #content based on event type
    if event_type == 'holiday':
        content = f"Upcoming holiday: {event_details}"
    elif event_type == 'exam':
        content = f"Upcoming exam : {event_details}"
    elif event_type == 'event':
        content = f"Event: {event_details}"
    else:
        content = "New notification"
    
    send_notification(id, content, recipient_type, recipient_id, event_type, event_details, db)
    
    return {"message": "Event notification sent successfully"}

#function to retrieve notification information
@app.get('/received_event_notification/{id}',tags=["Notifications"])
def received_event_notification(id: int, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(models.Notification.id == id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="notification not found")
    return {"Notification information": notification}


def send_notification_all(recipient_type: str, recipient_id: int, content: str, event_type: str, event_details: str, db: Session):
    notification = models.Notification(
        content=content,
        recipient_type=recipient_type,
        recipient_id=recipient_id,
        event_type=event_type,
        event_details=event_details
    )
    db.add(notification)
    db.commit()

#sending notification to one particular grade
@app.post('/send_notification/{grade_id}', tags=["Notifications"])
def send_grade_notification(grade_id: int, notification_request: schema.NotificationRequest, db: Session = Depends(get_db)):
    # Validate event_type 
    if notification_request.event_type not in ['holiday', 'exam', 'event']:
        raise HTTPException(status_code=400, detail="Invalid event type. Must be one of 'holiday', 'exam', or 'event'")
    
    # Query students in the specified grade
    students = db.query(models.Student).filter(models.Student.grade_id == grade_id).all()
    
    if not students:
        raise HTTPException(status_code=404, detail=f"No students found for grade id {grade_id}")
    
    #prepare content based on event_type
    content = notification_request.content
    if notification_request.event_type == 'holiday':
        content = f"Upcoming holiday: {notification_request.event_details}"
    elif notification_request.event_type == 'exam':
        content = f"Upcoming exam : {notification_request.event_details}"
    elif notification_request.event_type == 'event':
        content = f"Event: {notification_request.event_details}"
    
    #send notifications to each student
    for student in students:
        send_notification_all('student', student.id, content, notification_request.event_type, notification_request.event_details, db)
    
    return {"message": f"{len(students)} students in grade {grade_id} notified successfully"}
