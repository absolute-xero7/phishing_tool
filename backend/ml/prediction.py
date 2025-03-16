import os
import joblib
from ml.feature_extraction import FeatureExtractor

class PhishingPredictor:
    """Phishing prediction utility for the API."""
    
    def __init__(self, model_path):
        """Initialize with the path to the trained model."""
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_extractor = FeatureExtractor()
        self.load_model()
    
    def load_model(self):
        """Load the trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        # Load model and scaler
        self.model, self.scaler = joblib.load(self.model_path)
        print(f"Model loaded from {self.model_path}")
    
    def predict_url(self, url, fetch_content=True):
        """Predict if a URL is phishing."""
        if self.model is None:
            raise ValueError("Model not loaded!")
        
        # Extract features
        feature_vector, feature_dict = self.feature_extractor.extract_features(url, fetch_content)
        
        # Scale features
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # Make prediction
        is_phishing = self.model.predict(feature_vector_scaled)[0]
        confidence = self.model.predict_proba(feature_vector_scaled)[0][1]
        
        # Adjust confidence based on the prediction
        if is_phishing:
            confidence = confidence
        else:
            confidence = 1 - confidence
        
        return {
            'url': url,
            'is_phishing': bool(is_phishing),
            'confidence': float(confidence),
            'features': feature_dict
        }
    
    def predict_email(self, subject, sender, body):
        """Predict if an email is phishing."""
        if self.model is None:
            raise ValueError("Model not loaded!")
        
        # Extract features from email
        email_features = self.feature_extractor.extract_features_from_email(subject, sender, body)
        
        # Extract URLs from email body for additional analysis
        import re
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body)
        
        # If URLs found, analyze the most suspicious one
        url_results = []
        for url in urls:
            try:
                url_result = self.predict_url(url, fetch_content=False)
                url_results.append(url_result)
            except Exception as e:
                print(f"Error predicting URL {url}: {e}")
        
        # Sort URL results by phishing confidence
        url_results.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Determine email phishing status based on both content and URLs
        is_phishing = False
        confidence = 0.0
        
        # Check email content indicators
        content_indicators = [
            email_features['subject_has_urgent_words'],
            email_features['sender_has_domain_mismatch'],
            email_features['body_has_suspicious_links'],
            email_features['body_has_urgent_language'],
            email_features['body_requests_sensitive_info']
        ]
        
        # Simple rule-based model for email content
        content_score = sum(content_indicators) / len(content_indicators)
        
        # Combine with URL analysis if available
        if url_results:
            most_suspicious_url = url_results[0]
            combined_score = (content_score + most_suspicious_url['confidence']) / 2
            is_phishing = combined_score > 0.5 or most_suspicious_url['is_phishing']
            confidence = combined_score
        else:
            # Only use content analysis
            is_phishing = content_score > 0.4
            confidence = content_score
        
        return {
            'subject': subject,
            'sender': sender,
            'is_phishing': is_phishing,
            'confidence': confidence,
            'features': email_features,
            'analyzed_urls': url_results[:3] if url_results else []
        }