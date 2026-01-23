# NLP to SQL EdTech Backend Service

## Overview

This project implements an AI-powered backend service that allows non-technical users to query an EdTech database using natural language. The system converts English questions into SQL queries, executes them safely on a relational database, and returns the results along with performance metrics.

The application is built using FastAPI, SQLAlchemy, OpenAI-based NLP-to-SQL conversion, and is fully containerized using Docker and deployable on Kubernetes.

---

## Features

- Natural language to SQL query conversion using an LLM
- Secure SQL execution with SELECT-only enforcement
- FastAPI-based REST backend
- Relational database with realistic seeded data
- Query analytics and performance tracking
- Unit tests using pytest
- Dockerized application
- Kubernetes Pod configuration with resource limits

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI API
- pytest
- Docker
- Kubernetes (Docker Desktop)
- Spacy

---

## Project Structure

```
nlp_to_sql_edtech/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── nlp_to_sql.py
│   ├── analytics.py
│
├── tests/
│   ├── test_api.py
│   ├── test_nlp.py
│
├── pod.yaml
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── .env
├── README.md
```

---

## Database Schema

### Tables

**students**
- id
- name
- grade
- created_at

**courses**
- id
- name
- category

**enrollments**
- id
- student_id
- course_id
- enrolled_at

---

## API Endpoints

### POST /query

Converts a natural language question into SQL and returns the query result.

**Request**
```json
{
  "question": "How many students enrolled in Python courses?"
}
```

**Response**
```json
{
  "question": "How many students enrolled in Python courses?",
  "generated_sql": "SELECT COUNT(DISTINCT e.student_id) ...",
  "result": 7,
  "execution_time_ms": 2899.04
}
```

---

### GET /stats

Returns analytics about system usage.

**Response**
```json
{
  "total_queries": 5,
  "most_common_keywords": [
    ["enrolled", 3],
    ["python", 1]
  ],
  "slowest_query": {
    "question": "How many students enrolled in AI courses?",
    "execution_time_ms": 3971.61
  }
}
```

---

## NLP to SQL Approach

The NLP-to-SQL system uses a large language model to generate SQL queries based on the user question and database schema. A strict validation layer ensures that only SELECT queries are executed, and any potentially destructive SQL statements are blocked.

The LLM output is sanitized to remove markdown or explanatory text before validation and execution.

---

## Security Considerations

- Only SELECT queries are permitted
- SQL validation blocks DELETE, DROP, UPDATE, INSERT, and ALTER statements
- SQL execution is handled through SQLAlchemy
- API keys are managed via environment variables

---

## Running Locally (Without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variable:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

4. Open:
```
http://localhost:8000/docs
```

---

## Running with Docker

### Build Image
```bash
docker build -t nlp-to-sql-edtech .
```

### Run Container
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your_api_key_here nlp-to-sql-edtech
```

---

## Running on Kubernetes

### Prerequisites
- Docker Desktop with Kubernetes enabled
- kubectl configured

### Deploy Pod
```bash
kubectl apply -f pod.yaml
```

### Verify Pod
```bash
kubectl get pods
```

### Access Application
```bash
kubectl port-forward pod/nlp-to-sql-pod 8000:8000
```

Open:
```
http://localhost:8000/docs
```

---

## Testing

Run unit tests using pytest:

```bash
pytest -v
```
---

## Submission Checklist

- FastAPI application
- NLP-to-SQL implementation
- Secure SQL execution
- Analytics endpoint
- Unit tests
- Dockerfile
- Kubernetes Pod YAML
- Documentation
