from flask import Blueprint, jsonify, request

from graph.workflow import RAGWorkflow
from utils.exceptions import ApplicationError


agent_bp = Blueprint(
    "agent",
    __name__
)


rag_workflow = RAGWorkflow()


@agent_bp.route(
    "/api/agent/query",
    methods=["POST"]
)
def agent_query():

    data = request.get_json(
        silent=True
    )

    if not data or "question" not in data:

        raise ApplicationError(
            "Question is required.",
            400
        )

    result = rag_workflow.run(
        data["question"]
    )

    return jsonify({
        "success": True,
        "message": "Agent query completed.",
        "data": {
            "answer": result.get(
                "answer",
                "I could not find enough information."
            )
        }
    }), 200