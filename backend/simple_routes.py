from flask import Blueprint, jsonify, request
from database.models import URL, Email
from datetime import datetime, timedelta

# Create a Blueprint for API routes
simple_api_bp = Blueprint('simple_api', __name__)

@simple_api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

@simple_api_bp.route('/stats', methods=['GET'])
def stats():
    """Get phishing detection statistics."""
    try:
        # Count URLs
        total_urls = URL.query.count()
        phishing_urls = URL.query.filter_by(is_phishing=True).count()
        legitimate_urls = URL.query.filter_by(is_phishing=False).count()
        
        # Count emails
        total_emails = Email.query.count()
        phishing_emails = Email.query.filter_by(is_phishing=True).count()
        legitimate_emails = Email.query.filter_by(is_phishing=False).count()
        
        # Calculate percentages
        url_phishing_percentage = (phishing_urls / total_urls * 100) if total_urls > 0 else 0
        email_phishing_percentage = (phishing_emails / total_emails * 100) if total_emails > 0 else 0
        
        return jsonify({
            'urls': {
                'total': total_urls,
                'phishing': phishing_urls,
                'legitimate': legitimate_urls,
                'phishing_percentage': url_phishing_percentage
            },
            'emails': {
                'total': total_emails,
                'phishing': phishing_emails,
                'legitimate': legitimate_emails,
                'phishing_percentage': email_phishing_percentage
            }
        })
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@simple_api_bp.route('/url-history', methods=['GET'])
def url_history():
    """Get recent URL check history."""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get most recent URL checks
        recent_urls = URL.query.order_by(URL.checked_at.desc()).limit(limit).all()
        
        # Convert to JSON-serializable format
        history = []
        for url in recent_urls:
            history.append({
                'id': url.id,
                'url': url.url,
                'is_phishing': url.is_phishing,
                'confidence': url.confidence,
                'checked_at': url.checked_at.isoformat() if url.checked_at else datetime.now().isoformat()
            })
        
        return jsonify(history)
    except Exception as e:
        print(f"Error getting URL history: {e}")
        return jsonify({'error': str(e)}), 500

@simple_api_bp.route('/email-history', methods=['GET'])
def email_history():
    """Get recent email check history."""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Get most recent email checks
        recent_emails = Email.query.order_by(Email.checked_at.desc()).limit(limit).all()
        
        # Convert to JSON-serializable format
        history = []
        for email in recent_emails:
            history.append({
                'id': email.id,
                'subject': email.subject,
                'sender': email.sender,
                'is_phishing': email.is_phishing,
                'confidence': email.confidence,
                'checked_at': email.checked_at.isoformat() if email.checked_at else datetime.now().isoformat()
            })
        
        return jsonify(history)
    except Exception as e:
        print(f"Error getting email history: {e}")
        return jsonify({'error': str(e)}), 500

# Add a simple URL checker endpoint
@simple_api_bp.route('/check-url', methods=['POST'])
def check_url():
    """Simple URL check endpoint."""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Simple logic to detect phishing URLs
        is_phishing = False
        confidence = 0.95
        
        if 'phish' in url or 'secure' in url or 'login' in url:
            is_phishing = True
            confidence = 0.85
        
        # Save to database
        new_url = URL(
            url=url,
            is_phishing=is_phishing,
            confidence=confidence,
            checked_at=datetime.now()
        )
        
        from database.models import db
        db.session.add(new_url)
        db.session.commit()
        
        return jsonify({
            'url': url,
            'is_phishing': is_phishing,
            'confidence': confidence,
            'features': {'url_length': len(url), 'has_secure': 'secure' in url}
        })
    except Exception as e:
        print(f"Error checking URL: {e}")
        return jsonify({'error': str(e)}), 500