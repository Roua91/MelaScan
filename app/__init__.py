from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask_cors import CORS
from .database import db

jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Talisman(app)  # Enforce HTTPS security policies
    CORS(app)  # Enable CORS for frontend requests

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    from .routes import main_bp
    from .auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
