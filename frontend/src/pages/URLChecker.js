import React, { useState } from 'react';
import axios from 'axios';
import { FaShieldAlt, FaLink, FaExclamationTriangle, FaCheckCircle, FaSpinner } from 'react-icons/fa';

const URLChecker = () => {
    const [url, setUrl] = useState('');
    const [fetchContent, setFetchContent] = useState(true);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!url) {
            setError('Please enter a URL');
            return;
        }

        // Simple URL validation
        if (!url.match(/^https?:\/\/.+/)) {
            setError('Please enter a valid URL starting with http:// or https://');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/check-url', {
                url,
                fetch_content: fetchContent
            });

            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to check URL. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Filter out important features for display
    const getImportantFeatures = (features) => {
        const importantFeatureNames = [
            'url_length', 'has_ip_address', 'has_at_symbol',
            'domain_length', 'has_https', 'has_suspicious_tld',
            'has_login_form', 'has_password_field', 'has_suspicious_title'
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
            <h1>URL Phishing Checker</h1>
            <p>Enter a URL to check if it's a potential phishing attempt</p>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="url">URL to Check</label>
                        <input
                            type="text"
                            id="url"
                            placeholder="https://example.com"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={fetchContent}
                                onChange={(e) => setFetchContent(e.target.checked)}
                            />
                            Fetch and analyze website content (more accurate, but slower)
                        </label>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? (
                            <>
                                <FaSpinner className="icon-spin" />
                                Analyzing URL...
                            </>
                        ) : (
                            <>
                                <FaShieldAlt />
                                Check URL
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
                                {result.is_phishing ? 'Potential Phishing Detected' : 'URL Appears Legitimate'}
                            </div>
                        </div>

                        <div className="result-url">{result.url}</div>

                        <div className="result-score">
                            Confidence: {Math.round(result.confidence * 100)}%
                        </div>

                        <div className="result-explanation">
                            {result.is_phishing ? (
                                <p>
                                    This URL shows characteristics commonly associated with phishing attempts.
                                    Be cautious about sharing any personal information on this site.
                                </p>
                            ) : (
                                <p>
                                    Our analysis indicates this URL is likely legitimate.
                                    However, always stay vigilant when sharing sensitive information online.
                                </p>
                            )}
                        </div>

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

export default URLChecker;