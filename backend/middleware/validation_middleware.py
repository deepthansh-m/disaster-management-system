from flask import request, jsonify


# Middleware for validating input data in requests
def validate_location_data(request_data):
    """
    Validates location data (name or point) provided by the user.
    Ensures that either a location name or coordinates are provided.
    """
    if 'location_name' not in request_data and 'coordinates' not in request_data:
        return False, "Location name or coordinates are required."
    return True, None


def validate_prediction_data(request_data):
    """
    Validates the data required for making a disaster prediction.
    Ensures that all necessary fields are included in the request.
    """
    required_fields = ['location_name', 'event_type', 'start_date', 'end_date']

    missing_fields = [field for field in required_fields if field not in request_data]

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    return True, None


def validation_middleware(request_type):
    """
    Middleware function that validates incoming requests based on the type.
    - 'location' validation checks for location data.
    - 'prediction' validation checks for prediction-related data.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get the JSON body from the request
            request_data = request.get_json()
            if not request_data:
                return jsonify({"status": "error", "message": "Request body is empty."}), 400

            # Validate based on request type
            if request_type == 'location':
                is_valid, error_message = validate_location_data(request_data)
            elif request_type == 'prediction':
                is_valid, error_message = validate_prediction_data(request_data)
            else:
                return jsonify({"status": "error", "message": "Unknown request type."}), 400

            # If validation fails, return error message
            if not is_valid:
                return jsonify({"status": "error", "message": error_message}), 400

            # Proceed to the next middleware/controller if validation passes
            return func(*args, **kwargs)

        return wrapper

    return decorator
