from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust the origins as needed

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tailor_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import and register the routes
    from .routes import main
    app.register_blueprint(main)

    return app
