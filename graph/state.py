from typing import TypedDict, List, Dict


class RAGState(TypedDict):

    question: str

    rewritten_question: str

    documents: List[Dict]

    context: str

    answer: str

    retry_count: int

    retrieval_success: bool