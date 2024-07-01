
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models, schema
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI()
models.Base.metadata.create_all(bind= engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Grade module
@app.post("/grades/", tags=["Grade"])
def create_grade(grade : schema.grade, db: Session = Depends(get_db)):
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
    name = str(stud.name)
    if len(name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
    
    stud.name = stud.name.capitalize()
    new_student = models.Student(**stud.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get('/students/{id}', tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    student_info = db.query(models.Student).filter(models.Student.id == id).first()
    if student_info is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"Student information": student_info}

@app.get("/student_with_teacher/{grade_id}", response_model=list[schema.StudentWithTeacher], tags=["Student_with_Teacher"])
def get_StudentWithTeachers(grade_id : int, db: Session = Depends(get_db)):
    student_with_teacher =  db.query(models.Student.name.label("Student_name"),
                                     models.Grade.gradeName.label("Student_section"), 
                                     models.Teacher.name.label("Teacher_name"), 
                                     models.Teacher.qualification.label("Teacher_qualification")).join(models.Grade, models.Student.grade_id == models.Grade.id
    ).join(
         models.Grade, models.Teacher.grade_id == models.Grade.id
    ).filter(
        models.Grade.id == grade_id
    ).all()
    if not student_with_teacher:
        raise HTTPException(status_code=404, detail="No students found for the specified grade")
    
    return student_with_teacher

                            

@app.put('/stud/{id}', tags=["Students"])
def update_student(id: int, stud: Optional[schema.stud_update] = None, db: Session = Depends(get_db)):
    updated_stud = db.query(models.Student).filter(models.Student.id == id).first()
    if updated_stud is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if stud.name is not None:
        updated_stud.name = stud.name.capitalize()
    if stud.grade is not None:
        updated_stud.grade = stud.grade
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
    teaching.name = teaching.name.capitalize()
    new_teacher = models.Teacher(**teaching.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    print(new_teacher)
    return new_teacher

@app.get('/teachers/{id}', tags=["Teachers"])
def get_teacher(id: int, db: Session = Depends(get_db)):
    teacher_info = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if teacher_info is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"Teacher information": teacher_info}

@app.put('/teach/{id}', tags=["Teachers"])
def update_teach(id: int, teach: Optional[schema.teach_update] = None, db: Session = Depends(get_db)):
    updated_teach = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if updated_teach is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    if teach.name is not None:
        updated_teach.name = teach.name.capitalize()
    if teach.qualification is not None:
        updated_teach.teach = teach.quallification
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
