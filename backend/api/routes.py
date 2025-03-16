from flask import Blueprint, request, jsonify
from ml.prediction import PhishingPredictor
from database.operations import (
    save_url_check, get_url_history, get_url_stats,
    save_email_check, get_email_history, get_email_stats
)
import os
from config import Config

api_bp = Blueprint('api', __name__)

# Initialize predictor
predictor = None

@api_bp.before_app_first_request
def load_model():
    global predictor
    model_path = Config.MODEL_PATH
    
    # Check if model exists
    if not os.path.exists(model_path):
        # Create model directory
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Train model if it doesn't exist
        from ml.model_training import PhishingDetectionModel
        import pandas as pd
        
        model = PhishingDetectionModel()
        
        # Create sample dataset if it doesn't exist
        dataset_path = os.path.join(os.path.dirname(os.path.dirname(model_path)), 'data/phishing_dataset.csv')
        if not os.path.exists(dataset_path):
            print(f"Dataset not found at {dataset_path}. Creating sample dataset...")
            
            # Create sample dataset
            sample_data = {
                'url': [
                    'https://google.com',
                    'https://facebook.com',
                    'https://apple.com',
                    'https://amaz0n-security-alert.com',
                    'https://login-paypal-secure.com',
                    'https://microsoft-verify.com',
                    'https://netflix.com',
                    'https://amazon.com',
                    'https://ebay.com',
                    'https://secure-banking-login.com'
                ],
                'is_phishing': [0, 0, 0, 1, 1, 1, 0, 0, 0, 1]
            }
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
            
            # Save sample dataset
            pd.DataFrame(sample_data).to_csv(dataset_path, index=False)
            print(f"Sample dataset created at {dataset_path}")
        
        # Load dataset and train model
        df = model.load_dataset(dataset_path)
        features_cache_path = os.path.join(os.path.dirname(dataset_path), 'features_cache.pkl')
        feature_df = model.extract_features_from_dataset(df, cache_path=features_cache_path)
        model.train(feature_df, hyperparameter_tuning=False)
        model.save_model(model_path)
    
    # Initialize predictor with the model
    predictor = PhishingPredictor(model_path)

@api_bp.route('/check-url', methods=['POST'])
def check_url():
    """Check if a URL is a phishing attempt."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    fetch_content = data.get('fetch_content', True)
    
    try:
        # Predict phishing status
        result = predictor.predict_url(url, fetch_content)
        
        # Save result to database
        save_url_check(
            url=result['url'],
            is_phishing=result['is_phishing'],
            confidence=result['confidence'],
            features=result['features']
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/check-email', methods=['POST'])
def check_email():
    """Check if an email is a phishing attempt."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    subject = data.get('subject', '')
    sender = data.get('sender', '')
    body = data.get('body', '')
    
    if not body:
        return jsonify({'error': 'Email body is required'}), 400
    
    try:
        # Predict phishing status
        result = predictor.predict_email(subject, sender, body)
        
        # Save result to database
        save_email_check(
            subject=result['subject'],
            sender=result['sender'],
            content=body,
            is_phishing=result['is_phishing'],
            confidence=result['confidence'],
            features=result['features']
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/url-history', methods=['GET'])
def url_history():
    """Get recent URL check history."""
    limit = request.args.get('limit', 10, type=int)
    
    try:
        history = get_url_history(limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/email-history', methods=['GET'])
def email_history():
    """Get recent email check history."""
    limit = request.args.get('limit', 10, type=int)
    
    try:
        history = get_email_history(limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats', methods=['GET'])
def stats():
    """Get phishing detection statistics."""
    try:
        url_statistics = get_url_stats()
        email_statistics = get_email_stats()
        
        return jsonify({
            'urls': url_statistics,
            'emails': email_statistics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})