from flask import jsonify

# Custom error handler for the application
def handle_error(error):
    # Default error message and status
    message = "An unexpected error occurred."
    status_code = 500

    # Handle different types of errors
    if isinstance(error, KeyError):
        message = "Missing required data in the request."
        status_code = 400
    elif isinstance(error, ValueError):
        message = "Invalid data format."
        status_code = 400
    elif isinstance(error, FileNotFoundError):
        message = "The requested file was not found."
        status_code = 404
    elif isinstance(error, PermissionError):
        message = "Permission denied."
        status_code = 403
    elif isinstance(error, TypeError):
        message = "Incorrect data type provided."
        status_code = 400

    # Return the error message and status code as a JSON response
    response = {
        "status": "error",
        "message": message
    }

    return jsonify(response), status_code


# Register the error handler with Flask app
def register_error_handlers(app):
    app.register_error_handler(Exception, handle_error)  # Catch all exceptions
    app.register_error_handler(404, handle_error)  # Handle 404 Not Found
    app.register_error_handler(400, handle_error)  # Handle 400 Bad Request
    app.register_error_handler(403, handle_error)  # Handle 403 Forbidden
    app.register_error_handler(500, handle_error)  # Handle 500 Internal Server Error
