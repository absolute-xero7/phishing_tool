import React from 'react';
import { FaShieldAlt, FaLock, FaCode, FaDatabase, FaServer, FaReact } from 'react-icons/fa';

const About = () => {
    return (
        <div className="about-page">
            <h1>About Phishing Detector</h1>

            <div className="card">
                <div className="card-title">Project Overview</div>
                <p>
                    This phishing detection tool uses machine learning to identify and flag potential
                    phishing attempts in URLs and emails. It analyzes various features and patterns
                    commonly associated with phishing to provide real-time protection against online threats.
                </p>
            </div>

            <div className="card">
                <div className="card-title">Key Features</div>
                <ul className="feature-list">
                    <li>
                        <FaShieldAlt className="feature-icon" />
                        <div className="feature-details">
                            <h3>Real-time Detection</h3>
                            <p>Analyze URLs and emails as they are received</p>
                        </div>
                    </li>
                    <li>
                        <FaLock className="feature-icon" />
                        <div className="feature-details">
                            <h3>Comprehensive Analysis</h3>
                            <p>Examines multiple factors including URL structure, domain age, content analysis, and more</p>
                        </div>
                    </li>
                    <li>
                        <FaDatabase className="feature-icon" />
                        <div className="feature-details">
                            <h3>Historical Tracking</h3>
                            <p>Maintains a database of analyzed URLs and emails for reference</p>
                        </div>
                    </li>
                </ul>
            </div>

            <div className="card">
                <div className="card-title">Technology Stack</div>
                <div className="tech-stack">
                    <div className="tech-item">
                        <FaCode className="tech-icon" />
                        <div className="tech-details">
                            <h3>Backend</h3>
                            <p>Python, Flask, Scikit-learn</p>
                        </div>
                    </div>
                    <div className="tech-item">
                        <FaDatabase className="tech-icon" />
                        <div className="tech-details">
                            <h3>Database</h3>
                            <p>PostgreSQL</p>
                        </div>
                    </div>
                    <div className="tech-item">
                        <FaReact className="tech-icon" />
                        <div className="tech-details">
                            <h3>Frontend</h3>
                            <p>React, Chart.js</p>
                        </div>
                    </div>
                    <div className="tech-item">
                        <FaServer className="tech-icon" />
                        <div className="tech-details">
                            <h3>Deployment</h3>
                            <p>Docker</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="card">
                <div className="card-title">How It Works</div>
                <div className="how-it-works">
                    <div className="step">
                        <div className="step-number">1</div>
                        <div className="step-content">
                            <h3>Feature Extraction</h3>
                            <p>
                                Extract over 20 features from URLs and email content, including domain characteristics,
                                text patterns, HTML analysis, and more.
                            </p>
                        </div>
                    </div>
                    <div className="step">
                        <div className="step-number">2</div>
                        <div className="step-content">
                            <h3>Machine Learning Analysis</h3>
                            <p>
                                Process features through a trained Random Forest classifier that determines
                                the likelihood of a phishing attempt.
                            </p>
                        </div>
                    </div>
                    <div className="step">
                        <div className="step-number">3</div>
                        <div className="step-content">
                            <h3>Risk Assessment</h3>
                            <p>
                                Generate a comprehensive risk score and explanation of the factors
                                that contributed to the classification.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="card">
                <div className="card-title">Disclaimer</div>
                <p>
                    This tool is designed as a supplementary security measure and should not replace
                    common-sense security practices. While it uses advanced techniques to detect phishing,
                    no solution can guarantee 100% detection rate. Always exercise caution when dealing with
                    suspicious communications.
                </p>
            </div>
        </div>
    );
};

export default About;