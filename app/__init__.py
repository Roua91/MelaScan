# initialze Flask app
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    # Import and register routes
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
