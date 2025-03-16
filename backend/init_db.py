from flask import Flask
from database.models import db, URL, Email
from config import config
import time
import sys

# Create a minimal Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize database
db.init_app(app)

# Function to initialize database with retry logic
def initialize_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if tables exist
        tables = db.engine.table_names()
        print(f"Tables in database: {tables}")
        
        # Add some sample data
        if 'urls' in tables and URL.query.count() == 0:
            print("Adding sample URL data...")
            sample_urls = [
                URL(url='https://www.google.com', is_phishing=False, confidence=0.95),
                URL(url='https://www.amazon.com', is_phishing=False, confidence=0.92),
                URL(url='http://phishing-example.com', is_phishing=True, confidence=0.88)
            ]
            db.session.add_all(sample_urls)
            db.session.commit()
            print(f"Added {len(sample_urls)} sample URLs")
        
        if 'emails' in tables and Email.query.count() == 0:
            print("Adding sample email data...")
            sample_emails = [
                Email(subject='Account Update', sender='support@example.com', content_hash='abc123', is_phishing=False, confidence=0.89),
                Email(subject='Urgent: Verify Account', sender='security@phishing.com', content_hash='def456', is_phishing=True, confidence=0.91)
            ]
            db.session.add_all(sample_emails)
            db.session.commit()
            print(f"Added {len(sample_emails)} sample emails")
        
    print("Database initialization complete!")

# Main execution
if __name__ == "__main__":
    initialize_database()