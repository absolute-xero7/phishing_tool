import os
import pandas as pd
import csv

def create_sample_dataset(output_path):
    """Create a sample dataset of phishing and legitimate URLs."""
    # Sample phishing URLs
    phishing_urls = [
        'http://paypal-secure-login.com',
        'http://security-chase.com/login',
        'http://bankofamerica.update-account.com',
        'http://amaz0n-account-verification.com',
        'http://appleid.apple.com.update-billing.com',
        'http://facebook-security-login.com/verify',
        'http://secure.bankofamerica.comx.ru',
        'http://microsoft-verify-account.com',
        'http://googledocs.login-secure.com',
        'http://wells-fargo-secure.account-update.com',
        'http://dropbox.download-documents.info',
        'http://netflix-verify-billing.com',
        'http://linkedin.security-update.info',
        'http://update-your-instagram.com',
        'http://twitter-account-security.com',
        'http://verify-your-paypal.com',
        'http://ebay-motors-payment.com',
        'http://apple-icloud-verification.com',
        'http://support-amazon.com',
        'http://174.129.35.134/login',
        'http://secure-chase.com-login.eu',
        'http://bankofamerica.com@phishing.ru',
        'http://verify-apple-icloud.com/login',
        'http://onlinebanking.banking.wellsfargo.update.com',
        'http://www.paypal.com.verification.net',
    ]
    
    # Sample legitimate URLs
    legitimate_urls = [
        'https://www.google.com',
        'https://www.amazon.com',
        'https://www.facebook.com',
        'https://www.apple.com',
        'https://www.microsoft.com',
        'https://www.netflix.com',
        'https://www.paypal.com',
        'https://www.ebay.com',
        'https://www.twitter.com',
        'https://www.instagram.com',
        'https://www.linkedin.com',
        'https://www.github.com',
        'https://www.reddit.com',
        'https://www.nytimes.com',
        'https://www.cnn.com',
        'https://www.wikipedia.org',
        'https://www.youtube.com',
        'https://www.dropbox.com',
        'https://www.spotify.com',
        'https://www.bankofamerica.com',
        'https://www.chase.com',
        'https://www.wellsfargo.com',
        'https://www.airbnb.com',
        'https://www.walmart.com',
        'https://www.target.com',
    ]
    
    # Create DataFrame
    data = []
    
    # Add phishing URLs
    for url in phishing_urls:
        data.append({'url': url, 'is_phishing': 1})
    
    # Add legitimate URLs
    for url in legitimate_urls:
        data.append({'url': url, 'is_phishing': 0})
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"Sample dataset created with {len(df)} URLs ({len(phishing_urls)} phishing, {len(legitimate_urls)} legitimate)")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    create_sample_dataset('data/phishing_dataset.csv')