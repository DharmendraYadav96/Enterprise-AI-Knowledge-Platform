from flask import Blueprint, jsonify, request

from services.ingestion_service import IngestionService
from utils.exceptions import ApplicationError


ingestion_bp = Blueprint(
    "ingestion",
    __name__
)

ingestion_service = IngestionService()


@ingestion_bp.route(
    "/api/documents/process",
    methods=["POST"]
)
def process_document():

    data = request.get_json()

    if not data or "file_path" not in data:
        raise ApplicationError(
            "File path is required.",
            400
        )

    result = ingestion_service.process_document(
        data["file_path"]
    )

    return jsonify({
        "success": True,
        "message": "Document processed successfully.",
        "data": {
            "file_path": result["file_path"],
            "character_count": result["character_count"],
            "chunk_count": result["chunk_count"],
            "chunks": result["chunks"]
        }
    }), 200