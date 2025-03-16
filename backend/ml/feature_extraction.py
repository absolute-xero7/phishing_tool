import re
import tldextract
import requests
import numpy as np
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class FeatureExtractor:
    """Extract features from URLs and website content for phishing detection."""
    
    def __init__(self):
        self.feature_names = [
            # URL-based features
            'url_length', 'num_digits', 'num_special_chars', 'has_ip_address',
            'has_at_symbol', 'has_double_slash', 'domain_length', 'num_subdomains',
            'has_https', 'domain_age_days', 'has_suspicious_tld',
            # Content-based features
            'has_login_form', 'num_external_links', 'num_iframes', 'has_password_field',
            'form_to_link_ratio', 'has_favicon', 'has_suspicious_title',
            'has_misspelled_domains', 'has_hidden_elements'
        ]
    
    def extract_features_from_url(self, url):
        """Extract features from URL string."""
        features = {}
        
        # Basic URL features
        features['url_length'] = len(url)
        features['num_digits'] = sum(c.isdigit() for c in url)
        features['num_special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
        features['has_ip_address'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
        features['has_at_symbol'] = 1 if '@' in url else 0
        features['has_double_slash'] = 1 if '//' in url[8:] else 0
        
        # Domain-based features
        parsed_url = urlparse(url)
        features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
        
        # Use tldextract to get domain information
        extract_result = tldextract.extract(url)
        domain = extract_result.domain
        suffix = extract_result.suffix
        subdomain = extract_result.subdomain
        
        features['domain_length'] = len(domain)
        features['num_subdomains'] = len(subdomain.split('.')) if subdomain else 0
        
        # List of suspicious TLDs often used for phishing
        suspicious_tlds = ['xyz', 'top', 'link', 'work', 'date', 'ml', 'gq', 'ga', 'cf']
        features['has_suspicious_tld'] = 1 if suffix in suspicious_tlds else 0
        
        # Placeholder for domain age - in real system, this would query WHOIS databases
        features['domain_age_days'] = 365  # Default value, should be replaced with actual age
        
        return features
    
    def extract_features_from_content(self, url):
        """Extract features from webpage content."""
        features = {}
        
        try:
            # Set a timeout and user-agent to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for login forms
            forms = soup.find_all('form')
            login_keywords = ['login', 'signin', 'sign in', 'sign-in', 'log in', 'log-in', 'authenticate']
            features['has_login_form'] = 0
            
            for form in forms:
                form_text = str(form).lower()
                if any(keyword in form_text for keyword in login_keywords):
                    features['has_login_form'] = 1
                    break
            
            # Count external links
            base_domain = tldextract.extract(url)
            base_domain = f"{base_domain.domain}.{base_domain.suffix}"
            
            external_links = 0
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link['href']
                if href.startswith('http'):
                    link_domain = tldextract.extract(href)
                    link_domain = f"{link_domain.domain}.{link_domain.suffix}"
                    if link_domain != base_domain:
                        external_links += 1
            
            features['num_external_links'] = external_links
            
            # Count iframes
            features['num_iframes'] = len(soup.find_all('iframe'))
            
            # Check for password fields
            password_fields = soup.find_all('input', {'type': 'password'})
            features['has_password_field'] = 1 if password_fields else 0
            
            # Form to link ratio
            num_forms = len(forms)
            num_links = len(all_links)
            features['form_to_link_ratio'] = num_forms / num_links if num_links > 0 else 0
            
            # Check for favicon
            features['has_favicon'] = 1 if soup.find('link', rel=lambda r: r and 'icon' in r.lower()) else 0
            
            # Check title for suspicious keywords
            title = soup.title.string.lower() if soup.title else ''
            suspicious_title_keywords = ['login', 'sign in', 'verify', 'secure', 'account', 'update', 'confirm']
            features['has_suspicious_title'] = 1 if any(keyword in title for keyword in suspicious_title_keywords) else 0
            
            # Check for misspelled domains of popular websites
            popular_domains = ['google', 'facebook', 'apple', 'amazon', 'microsoft', 'paypal', 'netflix']
            extracted_domain = tldextract.extract(url).domain.lower()
            
            features['has_misspelled_domains'] = 0
            for domain in popular_domains:
                # Check for similar but not exact match
                if domain != extracted_domain and domain in extracted_domain:
                    # Use Levenshtein distance or similar algorithm for better detection
                    if len(domain) > 4 and len(extracted_domain) > 4:
                        features['has_misspelled_domains'] = 1
                        break
            
            # Check for hidden elements
            hidden_elements = soup.find_all(style=lambda s: s and 'display:none' in s.lower())
            hidden_elements += soup.find_all(style=lambda s: s and 'visibility:hidden' in s.lower())
            hidden_elements += soup.find_all(hidden=True)
            features['has_hidden_elements'] = 1 if hidden_elements else 0
            
        except Exception as e:
            print(f"Error extracting content features from {url}: {e}")
            # Set default values if fetch fails
            features['has_login_form'] = 0
            features['num_external_links'] = 0
            features['num_iframes'] = 0
            features['has_password_field'] = 0
            features['form_to_link_ratio'] = 0
            features['has_favicon'] = 1  # Most legitimate sites have favicons
            features['has_suspicious_title'] = 0
            features['has_misspelled_domains'] = 0
            features['has_hidden_elements'] = 0
        
        return features
    
    def extract_features(self, url, fetch_content=True):
        """Extract all features from URL and optionally its content."""
        # First get URL-based features
        features = self.extract_features_from_url(url)
        
        # Then add content-based features if requested
        if fetch_content:
            content_features = self.extract_features_from_content(url)
            features.update(content_features)
        else:
            # Set default values for content features
            default_content_features = {
                'has_login_form': 0,
                'num_external_links': 0,
                'num_iframes': 0,
                'has_password_field': 0,
                'form_to_link_ratio': 0,
                'has_favicon': 1,
                'has_suspicious_title': 0,
                'has_misspelled_domains': 0,
                'has_hidden_elements': 0
            }
            features.update(default_content_features)
        
        # Ensure all features are present in the correct order
        feature_vector = [features.get(feature_name, 0) for feature_name in self.feature_names]
        return feature_vector, features
    
    def extract_features_from_email(self, subject, sender, body):
        """Extract features from email content."""
        features = {}
        
        # Analyze subject
        features['subject_length'] = len(subject)
        features['subject_has_urgent_words'] = 0
        urgent_words = ['urgent', 'immediate', 'alert', 'verify', 'suspended', 'restricted', 'warning']
        if any(word in subject.lower() for word in urgent_words):
            features['subject_has_urgent_words'] = 1
        
        # Analyze sender
        features['sender_has_domain_mismatch'] = 0
        if '@' in sender:
            display_name = sender.split('<')[0].strip() if '<' in sender else ''
            email_address = sender.split('<')[1].split('>')[0] if '<' in sender else sender
            
            if display_name and '@' in email_address:
                display_domain = ''.join(c for c in display_name if c.isalnum() or c == '.').lower()
                email_domain = email_address.split('@')[1].lower()
                
                # Check if display name contains a domain different from email domain
                popular_domains = ['google', 'facebook', 'apple', 'amazon', 'microsoft', 'paypal', 'netflix']
                for domain in popular_domains:
                    if domain in display_domain and domain not in email_domain:
                        features['sender_has_domain_mismatch'] = 1
                        break
        
        # Analyze body
        features['body_length'] = len(body)
        features['body_has_suspicious_links'] = 0
        
        # Extract URLs from body
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body)
        features['num_links'] = len(urls)
        
        for url in urls:
            url_features = self.extract_features_from_url(url)
            if url_features['has_suspicious_tld'] or url_features['has_ip_address']:
                features['body_has_suspicious_links'] = 1
                break
        
        features['body_has_html'] = 1 if '<html' in body.lower() or '<body' in body.lower() else 0
        
        # Check for common phishing indicators
        features['body_has_urgent_language'] = 0
        urgent_phrases = ['account suspended', 'verify your account', 'security alert', 
                         'unauthorized access', 'limited time', 'act now', 'click here']
        
        if any(phrase in body.lower() for phrase in urgent_phrases):
            features['body_has_urgent_language'] = 1
        
        features['body_has_attachments'] = 1 if 'Content-Disposition: attachment' in body else 0
        
        # Check for request for sensitive information
        sensitive_phrases = ['password', 'credit card', 'update your information', 'confirm your details',
                           'social security', 'bank account', 'click the link']
        
        features['body_requests_sensitive_info'] = 0
        if any(phrase in body.lower() for phrase in sensitive_phrases):
            features['body_requests_sensitive_info'] = 1
        
        return features