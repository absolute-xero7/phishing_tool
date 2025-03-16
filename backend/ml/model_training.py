import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
from feature_extraction import FeatureExtractor

class PhishingDetectionModel:
    """Train and evaluate a phishing detection model."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_extractor = FeatureExtractor()
    
    def load_dataset(self, csv_path):
        """Load phishing dataset from CSV file."""
        # Expected CSV format:
        # url,is_phishing
        # http://example.com,0
        # http://phishing-example.com,1
        
        df = pd.read_csv(csv_path)
        print(f"Loaded dataset with {len(df)} samples")
        return df
    
    def extract_features_from_dataset(self, df, cache_path=None):
        """Extract features for all URLs in the dataset."""
        # Check if cached features exist
        if cache_path and os.path.exists(cache_path):
            print(f"Loading cached features from {cache_path}")
            return pd.read_pickle(cache_path)
        
        # Extract features for each URL
        feature_vectors = []
        feature_dicts = []
        labels = []
        
        print(f"Extracting features for {len(df)} URLs")
        for idx, row in df.iterrows():
            if idx % 100 == 0:
                print(f"Processing URL {idx}/{len(df)}")
            
            url = row['url']
            is_phishing = row['is_phishing']
            
            try:
                # Extract URL-based features only to speed up training
                # Content-based features can be added for production
                feature_vector, feature_dict = self.feature_extractor.extract_features(url, fetch_content=False)
                
                feature_vectors.append(feature_vector)
                feature_dicts.append(feature_dict)
                labels.append(is_phishing)
            except Exception as e:
                print(f"Error extracting features for {url}: {e}")
        
        # Create feature dataframe
        feature_df = pd.DataFrame(feature_vectors, columns=self.feature_extractor.feature_names)
        feature_df['is_phishing'] = labels
        
        # Cache features if path provided
        if cache_path:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            feature_df.to_pickle(cache_path)
            print(f"Cached features to {cache_path}")
        
        return feature_df
    
    def train(self, feature_df, hyperparameter_tuning=False):
        """Train the phishing detection model."""
        # Split features and target
        X = feature_df.drop('is_phishing', axis=1)
        y = feature_df['is_phishing']
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        if hyperparameter_tuning:
            # Perform hyperparameter tuning
            print("Performing hyperparameter tuning...")
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            
            grid_search = GridSearchCV(
                estimator=RandomForestClassifier(random_state=42),
                param_grid=param_grid,
                cv=3,
                n_jobs=-1,
                scoring='f1',
                verbose=2
            )
            
            grid_search.fit(X_train_scaled, y_train)
            
            # Get best model
            self.model = grid_search.best_estimator_
            print(f"Best parameters: {grid_search.best_params_}")
        else:
            # Train with default hyperparameters
            print("Training with default hyperparameters...")
            self.model = RandomForestClassifier(
                n_estimators=200, 
                max_depth=20, 
                min_samples_split=5,
                random_state=42
            )
            self.model.fit(X_train_scaled, y_train)
        
        # Evaluate on test set
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.4f}")
        
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Calculate feature importance
        feature_importances = pd.DataFrame(
            {'feature': X.columns, 'importance': self.model.feature_importances_}
        ).sort_values('importance', ascending=False)
        
        print("Top 10 Feature Importances:")
        print(feature_importances.head(10))
        
        return self.model, self.scaler
    
    def save_model(self, model_path):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model and scaler
        joblib.dump((self.model, self.scaler), model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """Load a trained model from disk."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model and scaler
        self.model, self.scaler = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        return self.model, self.scaler
    
    def predict(self, url, fetch_content=True):
        """Predict if a URL is phishing."""
        if self.model is None:
            raise ValueError("Model not loaded or trained yet!")
        
        # Extract features
        feature_vector, feature_dict = self.feature_extractor.extract_features(url, fetch_content)
        
        # Scale features
        feature_vector_scaled = self.scaler.transform([feature_vector])
        
        # Make prediction
        is_phishing = self.model.predict(feature_vector_scaled)[0]
        confidence = self.model.predict_proba(feature_vector_scaled)[0][1]
        
        return {
            'url': url,
            'is_phishing': bool(is_phishing),
            'confidence': float(confidence),
            'features': feature_dict
        }

if __name__ == "__main__":
    # Example usage
    model = PhishingDetectionModel()
    
    # Path to dataset
    dataset_path = "data/phishing_dataset.csv"
    
    # Check if dataset exists
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
    
    # Load dataset
    df = model.load_dataset(dataset_path)
    
    # Extract features
    features_cache_path = "data/features_cache.pkl"
    feature_df = model.extract_features_from_dataset(df, cache_path=features_cache_path)
    
    # Train model
    model.train(feature_df, hyperparameter_tuning=False)
    
    # Save model
    model_path = "ml/models/phishing_model.pkl"
    model.save_model(model_path)
    
    # Test prediction
    test_url = "https://suspicious-login-verification.com"
    result = model.predict(test_url, fetch_content=False)
    print(f"Prediction for {test_url}: {'Phishing' if result['is_phishing'] else 'Legitimate'} with {result['confidence']:.4f} confidence")