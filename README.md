# Phishing Detection Tool

A full-stack machine learning application that detects phishing attempts in URLs and emails, utilizing Python, PostgreSQL, React, and Docker.

![Phishing Detection Dashboard]()

## 🔍 Overview

This application provides real-time detection of phishing attempts through URL and email analysis. It uses machine learning to extract and analyze features commonly associated with phishing, presenting results through an intuitive dashboard.

### Key Features

- **URL Analysis**: Extract 20+ different features to identify phishing URLs
- **Email Analysis**: Detect phishing attempts in email content including links and suspicious phrases
- **Machine Learning**: Random Forest classifier for accurate prediction
- **Interactive Dashboard**: Visualize statistics and detection history
- **Responsive UI**: Modern interface optimized for both desktop and mobile

## 🛠️ Technology Stack

### Backend
- **Python/Flask**: RESTful API backend
- **scikit-learn**: Machine learning implementation
- **PostgreSQL**: Relational database for data storage
- **SQLAlchemy**: ORM for database operations

### Frontend
- **React**: Modern UI framework
- **Chart.js**: Data visualization
- **React Router**: Navigation and routing
- **Axios**: API communication

### Infrastructure
- **Docker**: Application containerization
- **Docker Compose**: Multi-container orchestration

## 🚀 Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phishing-detector.git
   cd phishing-detector
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:5000/api

## 📋 Usage Guide

### Checking URLs

1. Navigate to the URL Checker page
2. Enter the URL you want to analyze
3. Toggle "Fetch and analyze website content" for more accurate detection
4. Click "Check URL" to analyze
5. View results showing phishing probability and detection factors

### Checking Emails

1. Navigate to the Email Checker page
2. Enter the email subject, sender, and body content
3. Click "Check Email" to analyze
4. View results showing phishing probability and suspicious elements
5. See detected URLs and their analysis

### Dashboard

The dashboard provides an overview of:
- Total URLs and emails analyzed
- Phishing detection rates
- Recent detection history
- Detection trends over time

## 🔌 API Documentation

The application provides several RESTful API endpoints:

### Health Check
```
GET /api/health
```
Returns server status information.

### URL Analysis
```
POST /api/check-url
Content-Type: application/json

{
  "url": "https://example.com",
  "fetch_content": true
}
```
Analyzes a URL for phishing characteristics.

### Email Analysis
```
POST /api/check-email
Content-Type: application/json

{
  "subject": "Email subject",
  "sender": "sender@example.com",
  "body": "Email body content..."
}
```
Analyzes an email for phishing characteristics.

### Statistics
```
GET /api/stats
```
Returns detection statistics.

### History
```
GET /api/url-history?limit=10
GET /api/email-history?limit=10
```
Returns recent detection history.

## 📁 Project Structure

```
phishing-detector/
├── docker-compose.yml         # Docker Compose configuration
├── backend/                   # Python Flask backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── startup.sh             # Backend startup script
│   ├── simple_app.py          # Main Flask application
│   ├── simple_routes.py       # API routes
│   ├── init_db.py             # Database initialization
│   ├── api/                   # API modules
│   ├── database/              # Database models and operations
│   ├── ml/                    # Machine learning components
│   │   ├── feature_extraction.py
│   │   ├── model_training.py
│   │   └── prediction.py
│   └── utils/                 # Utility functions
├── frontend/                  # React frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/        # Reusable UI components
│       ├── pages/             # Application pages
│       ├── App.js             # Main React component
│       └── index.js           # React entry point
└── data/                      # Data storage
    └── postgres-data/         # PostgreSQL data volume
```

## 🧠 Machine Learning Approach

The phishing detection system uses a Random Forest classifier trained on the following feature categories:

1. **URL-based features**:
   - URL length, subdomain analysis, special character frequency
   - Domain age, IP address usage, suspicious TLDs
   - Protocol security (HTTP vs HTTPS)

2. **Content-based features**:
   - Presence of login forms and password fields
   - External link analysis
   - Hidden content detection
   - Brand imitation detection

3. **Email-specific features**:
   - Sender domain analysis
   - Urgent language detection
   - Sensitive information requests
   - Link analysis within email content

## 🌟 Future Enhancements

- **Browser Extension**: Real-time URL checking in web browsers
- **Advanced ML Models**: Implement neural networks for improved accuracy
- **User Accounts**: Add authentication and personalized history
- **API Access**: Provide API keys for third-party integration
- **Threat Intelligence**: Integrate with external phishing databases

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♀️ Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👏 Acknowledgements

- [Scikit-learn](https://scikit-learn.org/) for machine learning capabilities
- [Flask](https://flask.palletsprojects.com/) for the API framework
- [React](https://reactjs.org/) for the frontend UI
- [Docker](https://www.docker.com/) for containerization
- [Chart.js](https://www.chartjs.org/) for data visualization

---

💼 **Project created by [Your Name]** - [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourusername)