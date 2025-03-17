# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from .config import Config

# Initialize the MongoDB instance
mongo = PyMongo()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Load the configuration from the Config class
    app.config.from_object(Config)

    # Initialize MongoDB with Flask
    mongo.init_app(app)

    # Register blueprints for routes
    from app.routes import main_routes  # Ensure routes module exists
    app.register_blueprint(main_routes)

    # Return the app instance
    return app
