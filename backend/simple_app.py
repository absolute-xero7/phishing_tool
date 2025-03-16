from flask import Flask
from flask_cors import CORS
from database.models import db
from config import config
from simple_routes import simple_api_bp
import os

def create_app(config_name='development'):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Ensure the database URL is set correctly
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 
                                                        'postgresql://postgres:postgres@db:5432/phishing_detector')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(simple_api_bp, url_prefix='/api')
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created/verified.")
    
    return app

if __name__ == '__main__':
    print("Starting Flask application...")
    app = create_app()
    print("Flask application created, running on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)