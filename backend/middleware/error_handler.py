from flask import jsonify

def register_error_handlers(app):
    """Register global error handlers."""
    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({"status": "error", "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"status": "error", "message": "Internal server error"}), 500
