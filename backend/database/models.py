from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class URL(db.Model):
    """Model for storing URL check records."""
    
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    is_phishing = db.Column(db.Boolean, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    features = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<URL {self.url}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'is_phishing': self.is_phishing,
            'confidence': self.confidence,
            'checked_at': self.checked_at.isoformat(),
            'features': self.features
        }

class Email(db.Model):
    """Model for storing email check records."""
    
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(512), nullable=True)
    sender = db.Column(db.String(256), nullable=True)
    content_hash = db.Column(db.String(64), nullable=False, unique=True)
    is_phishing = db.Column(db.Boolean, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    features = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<Email {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'sender': self.sender,
            'is_phishing': self.is_phishing,
            'confidence': self.confidence,
            'checked_at': self.checked_at.isoformat(),
            'features': self.features
        }