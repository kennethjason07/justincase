from flask import Flask
from flask_cors import CORS
from back.models import db
from back.routes import main

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust the origins as needed

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tailor_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
