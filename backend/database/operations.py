import hashlib
from database.models import db, URL, Email

def save_url_check(url, is_phishing, confidence, features=None):
    """Save URL check result to database."""
    url_record = URL(
        url=url,
        is_phishing=is_phishing,
        confidence=confidence,
        features=features
    )
    db.session.add(url_record)
    db.session.commit()
    return url_record.to_dict()

def get_url_history(limit=10):
    """Get recent URL check history."""
    url_records = URL.query.order_by(URL.checked_at.desc()).limit(limit).all()
    return [record.to_dict() for record in url_records]

def get_url_stats():
    """Get URL check statistics."""
    total_urls = URL.query.count()
    phishing_urls = URL.query.filter_by(is_phishing=True).count()
    legitimate_urls = URL.query.filter_by(is_phishing=False).count()
    
    return {
        'total': total_urls,
        'phishing': phishing_urls,
        'legitimate': legitimate_urls,
        'phishing_percentage': (phishing_urls / total_urls * 100) if total_urls > 0 else 0
    }

def save_email_check(subject, sender, content, is_phishing, confidence, features=None):
    """Save email check result to database."""
    # Create a hash of the content to avoid saving duplicates
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Check if email already exists
    existing_email = Email.query.filter_by(content_hash=content_hash).first()
    if existing_email:
        return existing_email.to_dict()
    
    email_record = Email(
        subject=subject,
        sender=sender,
        content_hash=content_hash,
        is_phishing=is_phishing,
        confidence=confidence,
        features=features
    )
    db.session.add(email_record)
    db.session.commit()
    return email_record.to_dict()

def get_email_history(limit=10):
    """Get recent email check history."""
    email_records = Email.query.order_by(Email.checked_at.desc()).limit(limit).all()
    return [record.to_dict() for record in email_records]

def get_email_stats():
    """Get email check statistics."""
    total_emails = Email.query.count()
    phishing_emails = Email.query.filter_by(is_phishing=True).count()
    legitimate_emails = Email.query.filter_by(is_phishing=False).count()
    
    return {
        'total': total_emails,
        'phishing': phishing_emails,
        'legitimate': legitimate_emails,
        'phishing_percentage': (phishing_emails / total_emails * 100) if total_emails > 0 else 0
    }