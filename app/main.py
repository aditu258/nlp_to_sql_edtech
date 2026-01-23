from fastapi import FastAPI
from app.database import engine,SessionLocal
from app import models
from datetime import datetime
from fastapi import HTTPException
import time
from app.nlp_to_sql import nlp_to_sql
from sqlalchemy import text
from app.analytics import record_query,get_stats

app=FastAPI(title="NLP to SQL EdTech API")

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def seed_database():
    db=SessionLocal()
    if db.query(models.Student).first():
        db.close()
        return 
    students=[
        models.Student(name="Aditya", grade="A"),
        models.Student(name="Rahul", grade="B"),
        models.Student(name="Sneha", grade="A"),
        models.Student(name="Aman", grade="C"),
        models.Student(name="Pooja", grade="B"),
        models.Student(name="Riya", grade="A"),
        models.Student(name="Kunal", grade="C"),
        models.Student(name="Neha", grade="B"),
        models.Student(name="Arjun", grade="A"),
        models.Student(name="Simran", grade="B"),
    ]   
    db.add_all(students)
    db.commit()
    
    courses=[
        models.Course(name="Python", category="Programming"),
        models.Course(name="Machine Learning", category="AI"),
        models.Course(name="Data Science", category="AI"),
        models.Course(name="SQL Basics", category="Database"),
        models.Course(name="Deep Learning", category="AI"),
    ]    
    db.add_all(courses)
    db.commit()

    enrollments=[
        models.Enrollment(student_id=1, course_id=1),
        models.Enrollment(student_id=2, course_id=1),
        models.Enrollment(student_id=3, course_id=1),
        models.Enrollment(student_id=4, course_id=2),
        models.Enrollment(student_id=5, course_id=3),
        models.Enrollment(student_id=6, course_id=1),
        models.Enrollment(student_id=7, course_id=4),
        models.Enrollment(student_id=8, course_id=2),
        models.Enrollment(student_id=9, course_id=1),
        models.Enrollment(student_id=10, course_id=5),
        models.Enrollment(student_id=1, course_id=2),
        models.Enrollment(student_id=2, course_id=3),
        models.Enrollment(student_id=3, course_id=4),
        models.Enrollment(student_id=4, course_id=5),
        models.Enrollment(student_id=5, course_id=1),
        models.Enrollment(student_id=6, course_id=2),
        models.Enrollment(student_id=7, course_id=3),
        models.Enrollment(student_id=8, course_id=4),
        models.Enrollment(student_id=9, course_id=5),
        models.Enrollment(student_id=10, course_id=1),
    ]
    db.add_all(enrollments)
    db.commit()
    db.close()
    

@app.post("/query")
def query_db(payload:dict):
    question=payload.get("question")
    if not question:
        raise HTTPException(status_code=400,detail="Question is required")
    start_time=time.time()
    sql,is_valid=nlp_to_sql(question)
    if not is_valid:
        raise HTTPException(status_code=400,detail="Invalid SQL query")
    db=SessionLocal()
    try:
        result=db.execute(text(sql))
        rows=result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        db.close()
    execution_time=round((time.time()-start_time)*1000,2)
    record_query(question,execution_time)
    
    if len(rows)==1 and len(rows[0])==1:
        final_result=rows[0][0]
    else:
        final_result=[dict(row._mapping) for row in rows]
    return {
        "question": question,
        "generated_sql": sql,
        "result": final_result,
        "execution_time_ms": execution_time
    }
    
@app.get("/stats")
def stats():
    return get_stats()
