from flask import Blueprint, jsonify, request

from services.rag_service import RAGService
from utils.exceptions import ApplicationError
from config import Config


rag_bp = Blueprint(
    "rag",
    __name__
)


rag_service = RAGService(
    api_key=Config.OPENAI_API_KEY
)


@rag_bp.route(
    "/api/rag/query",
    methods=["POST"]
)
def query_documents():

    data = request.get_json()

    if not data or "question" not in data:

        raise ApplicationError(
            "Question is required.",
            400
        )

    result = rag_service.answer_question(
        question=data["question"]
    )

    return jsonify({
        "success": True,
        "message": "Question answered successfully.",
        "data": result
    }), 200