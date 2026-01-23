from app.nlp_to_sql import validate_sql,nlp_to_sql

def test_validate_sql_select_only():
    assert validate_sql("SELECT * FROM students") is True
    assert validate_sql("DROP TABLE students") is False
    assert validate_sql("DELETE FROM students") is False

def test_nlp_to_sql_generates_select():
    sql, is_valid=nlp_to_sql("How many students enrolled in Python courses?")
    assert is_valid is True
    assert sql.lower().startswith("select")
