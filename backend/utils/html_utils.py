# HTML utility functions

def sanitize_html(html_content):
    """Sanitize HTML content."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup)

def extract_links(html_content):
    """Extract all links from HTML content."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])
    return links

def extract_forms(html_content):
    """Extract all forms from HTML content."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = []
    for form in soup.find_all('form'):
        forms.append(str(form))
    return forms

def has_login_form(html_content):
    """Check if HTML content contains a login form."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for forms with login-related attributes
    login_keywords = ['login', 'signin', 'sign in', 'sign-in', 'log in', 'log-in', 'authenticate']
    forms = soup.find_all('form')
    
    for form in forms:
        form_text = str(form).lower()
        if any(keyword in form_text for keyword in login_keywords):
            return True
        
        # Check for password fields
        if form.find('input', {'type': 'password'}):
            return True
    
    return False