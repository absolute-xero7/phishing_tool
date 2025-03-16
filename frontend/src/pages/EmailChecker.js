import React, { useState } from 'react';
import axios from 'axios';
import { FaShieldAlt, FaEnvelope, FaExclamationTriangle, FaCheckCircle, FaSpinner } from 'react-icons/fa';

const EmailChecker = () => {
    const [subject, setSubject] = useState('');
    const [sender, setSender] = useState('');
    const [body, setBody] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!body) {
            setError('Email body is required');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/check-email', {
                subject,
                sender,
                body
            });

            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to check email. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Format features for display
    const getImportantFeatures = (features) => {
        const importantFeatureNames = [
            'subject_has_urgent_words', 'sender_has_domain_mismatch',
            'body_has_suspicious_links', 'body_has_urgent_language',
            'body_requests_sensitive_info', 'subject_length',
            'body_has_html', 'num_links'
        ];

        return Object.entries(features)
            .filter(([key]) => importantFeatureNames.includes(key))
            .map(([key, value]) => {
                // Format feature name
                const formattedName = key
                    .split('_')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');

                return { name: formattedName, value };
            });
    };

    return (
        <div>
            <h1>Email Phishing Checker</h1>
            <p>Analyze email content to identify potential phishing attempts</p>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="subject">Email Subject</label>
                        <input
                            type="text"
                            id="subject"
                            placeholder="Enter email subject"
                            value={subject}
                            onChange={(e) => setSubject(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="sender">Sender</label>
                        <input
                            type="text"
                            id="sender"
                            placeholder="name@example.com"
                            value={sender}
                            onChange={(e) => setSender(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="body">Email Body</label>
                        <textarea
                            id="body"
                            placeholder="Paste the email content here"
                            value={body}
                            onChange={(e) => setBody(e.target.value)}
                            required
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? (
                            <>
                                <FaSpinner className="icon-spin" />
                                Analyzing Email...
                            </>
                        ) : (
                            <>
                                <FaShieldAlt />
                                Check Email
                            </>
                        )}
                    </button>
                </form>
            </div>

            {result && (
                <div className="result-section">
                    <h2>Analysis Result</h2>

                    <div className={`result-box ${result.is_phishing ? 'phishing' : 'legitimate'}`}>
                        <div className="result-header">
                            {result.is_phishing ? (
                                <FaExclamationTriangle size={24} color="#f44336" />
                            ) : (
                                <FaCheckCircle size={24} color="#4caf50" />
                            )}
                            <div className="result-title">
                                {result.is_phishing ? 'Potential Phishing Email Detected' : 'Email Appears Legitimate'}
                            </div>
                        </div>

                        <div className="result-email-details">
                            <div><strong>Subject:</strong> {result.subject || '(No subject)'}</div>
                            <div><strong>From:</strong> {result.sender || '(Unknown sender)'}</div>
                        </div>

                        <div className="result-score">
                            Confidence: {Math.round(result.confidence * 100)}%
                        </div>

                        <div className="result-explanation">
                            {result.is_phishing ? (
                                <p>
                                    This email shows characteristics commonly associated with phishing attempts.
                                    Be cautious about clicking any links or responding with personal information.
                                </p>
                            ) : (
                                <p>
                                    Our analysis indicates this email is likely legitimate.
                                    However, always stay vigilant when responding to emails requesting sensitive information.
                                </p>
                            )}
                        </div>

                        {result.analyzed_urls && result.analyzed_urls.length > 0 && (
                            <div className="analyzed-urls">
                                <h3>Detected URLs</h3>
                                <ul className="url-list">
                                    {result.analyzed_urls.map((url, index) => (
                                        <li key={index} className={url.is_phishing ? 'phishing-url' : 'legitimate-url'}>
                                            <div className="url-info">
                                                {url.url}
                                                <span className="url-status">
                                                    {url.is_phishing ? 'Suspicious' : 'Legitimate'}
                                                </span>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        <div className="feature-section">
                            <h3>Key Detection Factors</h3>
                            <div className="feature-list">
                                {result.features && getImportantFeatures(result.features).map((feature, index) => (
                                    <div key={index} className="feature-item">
                                        <div className="feature-name">{feature.name}</div>
                                        <div className="feature-value">
                                            {typeof feature.value === 'boolean' ?
                                                (feature.value ? 'Yes' : 'No') :
                                                (typeof feature.value === 'number' ?
                                                    feature.value :
                                                    String(feature.value))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EmailChecker;