from sqlalchemy import Column, Integer, String ,DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__="students"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    grade=Column(String)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
class Course(Base):
    __tablename__="courses"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    category=Column(String)
    
class Enrollment(Base):
    __tablename__="enrollments"
    id=Column(Integer,primary_key=True,index=True)
    student_id=Column(Integer,ForeignKey("students.id"))
    course_id=Column(Integer,ForeignKey("courses.id"))
    enrolled_at=Column(DateTime(timezone=True),server_default=func.now())
    
