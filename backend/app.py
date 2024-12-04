from flask import Flask
from backend.routes.disaster_routes import register_disaster_routes
from backend.routes.prediction_routes import register_prediction_routes
from backend.routes.weather_routes import weather_bp
from backend.middleware.error_handler import handle_error

def create_app():
    app = Flask(__name__)

    # Register routes
    register_disaster_routes(app)
    register_prediction_routes(app)
    app.register_blueprint(weather_bp)

    # Global error handler
    app.register_error_handler(Exception, handle_error)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
