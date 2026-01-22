from collections import Counter
from typing import Dict,Any
import re

analytics_store={
    "total_queries": 0,
    "slowest_query_ms": 0.0,
    "slowest_question": None,
    "keywords": Counter()
}

def extract_keywords(questions:str):
    stopwords = {
        "how", "many", "what", "is", "are", "the",
        "in", "of", "to", "for", "students", "courses"
    }
    questions = re.sub(r"[^\w\s]", "", questions.lower())
    words=questions.lower().split()
    keywords=[w for w in words if w not in stopwords]
    return keywords

def record_query(question:str,execution_time_ms:float):
    analytics_store["total_queries"]+=1
    if execution_time_ms > analytics_store["slowest_query_ms"]:
        analytics_store["slowest_query_ms"] = execution_time_ms
        analytics_store["slowest_question"] = question
    
    keywords=extract_keywords(question)
    analytics_store["keywords"].update(keywords)

def get_stats()->Dict[str,Any]:
    return {
        "total_queries":analytics_store["total_queries"],
        "most_common_keywords": analytics_store["keywords"].most_common(5),
        "slowest_query": {
            "question": analytics_store["slowest_question"],
            "execution_time_ms": analytics_store["slowest_query_ms"]
        }
    }