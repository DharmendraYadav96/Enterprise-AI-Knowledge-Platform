from flask import Flask, jsonify
from config import Config

from utils.logger import setup_logger
from utils.exceptions import ApplicationError

from routes.document_routes import document_bp
from routes.health_routes import health_bp
from routes.ingestion_routes import ingestion_bp
from routes.rag_routes import rag_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logger = setup_logger()

    app.register_blueprint(health_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(rag_bp)
    

    @app.errorhandler(ApplicationError)
    def handle_application_error(error):
        logger.error(
            "Application error: %s",
            error.message
        )

        return jsonify({
            "success": False,
            "message": error.message
        }), error.status_code

    @app.errorhandler(Exception)
    def handle_general_error(error):
        logger.exception("Unexpected error occurred")

        return jsonify({
            "success": False,
            "message": "An unexpected error occurred."
        }), 500

    logger.info("Flask application initialized")


    

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])