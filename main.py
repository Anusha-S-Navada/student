from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models, schema
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind= engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/")
def create_student(stud : schema.stud, db: Session = Depends(get_db)):
    new_student = models.Student(**stud.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return stud



@app.get('/students/{id}')
def get_student(id: int, db: Session = Depends(get_db)):
    student_info = db.query(models.Student).filter(models.Student.id == id).first()
    print(student_info)
    return {"Student information": student_info}

@app.put('/stud/{id}')
def update_student(id: int, stud: schema.stud_update, db: Session = Depends(get_db)):
    updated_stud = db.query(models.Student).filter(models.Student.id == id).first()
    if updated_stud is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if stud.name is not None:
        updated_stud.name = stud.name
    if stud.grade is not None:
        updated_stud.grade = stud.grade
    if stud.age is not None:
        updated_stud.age = stud.age
    db.commit()
    db.refresh(updated_stud)
    return updated_stud

@app.delete('/del_stud/{id}')
def delete_student(id:int, db:Session = Depends(get_db)):
    deleted_student = db.query(models.Student).filter(models.Student.id == id).first()
    if deleted_student is None:
         raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(deleted_student)
    db.commit()
    return {f'student of id:{id} deleted successfully'}