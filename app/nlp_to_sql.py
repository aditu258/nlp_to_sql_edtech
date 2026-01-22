import os
import re
from typing import Tuple
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_SCHEMA=""" 
Tables:
students(id, name, grade, created_at)
courses(id, name, category)
enrollments(id, student_id, course_id, enrolled_at)

Relationships:
students.id = enrollments.student_id
courses.id = enrollments.course_id
"""

def validate_sql(sql:str)->bool:
    sql=sql.strip().lower()
    forbidden = ["delete", "drop", "update", "insert", "alter", "truncate"]
    if not sql.startswith("select"):
        return False
    for word in forbidden:
        if word in sql:
            return False
    return True

def openai_generate_sql(question:str)->str:
    prompt=f"""
You are an expert SQL generator.

Rules:
- Generate ONLY SELECT queries
- Do NOT use DELETE, UPDATE, DROP, INSERT
- Use correct JOINs based on schema
- Return ONLY SQL, no explanation

Database Schema:
{DB_SCHEMA}

Question:
{question}
"""

    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a helpful assistant that writes SQL queries."},
            {"role":"user","content":prompt}
        ],
        temperature=0
    )
    sql=response.choices[0].message.content.strip()
    return sql

def nlp_to_sql(question:str)->Tuple[str,bool]:
    raw_sql=openai_generate_sql(question)
    sql=clean_sql(raw_sql)
    is_valid=validate_sql(sql)
    return sql,is_valid

def clean_sql(sql:str)->str:
    sql=sql.strip()
    sql=re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql=re.sub(r"```", "", sql)
    
    match=re.search(r"(select .*;?)", sql, re.IGNORECASE | re.DOTALL)
    if match:
        sql=match.group(1)
    return sql.strip()