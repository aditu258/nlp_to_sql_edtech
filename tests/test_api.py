from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_query_endpoint():
    response=client.post(
        "/query",
        json={"question": "How many students enrolled in Python courses?"}
    )
    assert response.status_code == 200
    data=response.json()
    assert "generated_sql" in data
    assert "result" in data
    assert "execution_time_ms" in data

def test_stats_endpoint():
    response=client.get("/stats")
    assert response.status_code == 200
    data=response.json()
    assert "total_queries" in data
    assert "most_common_keywords" in data
    assert "slowest_query" in data
