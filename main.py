from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models, schema
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
    if len(stud.name.strip()) < 3:
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


@app.put('/stud/{id}', tags=["Students"])
def update_student(id: int, stud: schema.stud_update, db: Session = Depends(get_db)):
    updated_stud = db.query(models.Student).filter(models.Student.id == id).first()
    if updated_stud is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
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
    if len(teaching.name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
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
@app.get("/students_by_grade/{grade_id}")
def get_students_by_grade(grade_id: int, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.grade_id == grade_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for the specified grade")
    return students

#getting teachers information using grade id
@app.get("/teachers_by_grade/{grade_id}")
def get_teachers_by_grade(grade_id: int, db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).filter(models.Teacher.grade_id == grade_id).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="No students found for the specified grade")
    return teachers

#getting students and teachers information using grade id             
@app.get("/grade_info/{grade_id}", response_model=dict)
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
@app.get('/count_students/{grade_id}')
def count_students(grade_id: int, db: Session = Depends(get_db)):
    count = db.query(models.Student).filter(models.Student.grade_id == grade_id).count()
    return {"grade_id": grade_id, "Total_student_count": count}


#counting total number of tudents in particular grade
@app.get('/count_teachers/{grade_id}')
def count_teachers(grade_id: int, db: Session = Depends(get_db)):
    count = db.query(models.Teacher).filter(models.Teacher.grade_id == grade_id).count()
    return {"grade_id": grade_id,"Total_teachers_count": count}