from app import app
from models import db

# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
