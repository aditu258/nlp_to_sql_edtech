from collections import Counter
from typing import Dict, Any, List
import spacy

nlp=spacy.load("en_core_web_sm")

analytics_store={
    "total_queries":0,
    "slowest_query_ms":0.0,
    "slowest_question":None,
    "keywords":Counter()
}

ALLOWED_POS={"NOUN","PROPN","VERB"}

def extract_keywords(question:str) -> List[str]:
    doc=nlp(question.lower())

    keywords=[
        token.text
        for token in doc
        if token.pos_ in ALLOWED_POS and token.is_alpha
    ]

    return keywords


def record_query(question:str,execution_time_ms:float):
    analytics_store["total_queries"]+=1

    if execution_time_ms > analytics_store["slowest_query_ms"]:
        analytics_store["slowest_query_ms"]=execution_time_ms
        analytics_store["slowest_question"]=question

    analytics_store["keywords"].update(extract_keywords(question))


def get_stats()->Dict[str,Any]:
    return {
        "total_queries":analytics_store["total_queries"],
        "most_common_keywords":analytics_store["keywords"].most_common(5),
        "slowest_query":{
            "question":analytics_store["slowest_question"],
            "execution_time_ms":analytics_store["slowest_query_ms"]
        }
    }
