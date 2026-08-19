from flask import Blueprint, jsonify, request

from services.document_service import DocumentService


document_bp = Blueprint("documents", __name__)

document_service = DocumentService(
    upload_folder="data/uploads"
)


@document_bp.route("/api/documents/upload", methods=["POST"])
def upload_document():

    file = request.files.get("file")

    result = document_service.upload_document(file)

    return jsonify({
        "success": True,
        "message": "Document uploaded successfully.",
        "data": result
    }), 201