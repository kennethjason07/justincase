from back.app import app
from back.models import db

# Ensure the database is initialized when the application starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
