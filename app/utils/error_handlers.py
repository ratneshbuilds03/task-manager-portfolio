from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(_error):
        return jsonify({"error": "Authentication required"}), 401

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.description}), error.code

        from app import db

        db.session.rollback()
        current_app.logger.exception("Unhandled application exception")
        return jsonify({"error": "Internal server error"}), 500
