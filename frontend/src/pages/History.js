import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaHistory, FaLink, FaEnvelope, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';

const History = () => {
    const [activeTab, setActiveTab] = useState('urls');
    const [urlHistory, setUrlHistory] = useState([]);
    const [emailHistory, setEmailHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchHistory = async () => {
            setLoading(true);
            setError(null);

            try {
                if (activeTab === 'urls') {
                    const response = await axios.get('/api/url-history?limit=20');
                    setUrlHistory(response.data);
                } else {
                    const response = await axios.get('/api/email-history?limit=20');
                    setEmailHistory(response.data);
                }
            } catch (err) {
                setError('Failed to fetch history. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchHistory();
    }, [activeTab]);

    // Format date for display
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString();
    };

    // Truncate long URLs or subjects for display
    const truncate = (str, maxLength = 50) => {
        if (!str) return '';
        return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
    };

    return (
        <div>
            <h1>Detection History</h1>

            <div className="tabs">
                <button
                    className={`tab ${activeTab === 'urls' ? 'active' : ''}`}
                    onClick={() => setActiveTab('urls')}
                >
                    <FaLink />
                    URL History
                </button>
                <button
                    className={`tab ${activeTab === 'emails' ? 'active' : ''}`}
                    onClick={() => setActiveTab('emails')}
                >
                    <FaEnvelope />
                    Email History
                </button>
            </div>

            {loading ? (
                <div className="loading">Loading history...</div>
            ) : error ? (
                <div className="error">{error}</div>
            ) : (
                <div className="history-container">
                    {activeTab === 'urls' ? (
                        <div className="url-history">
                            <h2>URL Check History</h2>

                            {urlHistory.length === 0 ? (
                                <div className="no-history">No URL check history available</div>
                            ) : (
                                <div className="history-list">
                                    {urlHistory.map((item) => (
                                        <div key={item.id} className="history-item">
                                            <div className="history-item-content">
                                                <div className="history-url">{item.url}</div>
                                                <div className="history-date">{formatDate(item.checked_at)}</div>
                                            </div>
                                            <div className="history-result">
                                                {item.is_phishing ? (
                                                    <div className="phishing-result">
                                                        <FaExclamationTriangle color="#f44336" />
                                                        <span>Phishing</span>
                                                        <span className="confidence">
                                                            ({Math.round(item.confidence * 100)}%)
                                                        </span>
                                                    </div>
                                                ) : (
                                                    <div className="legitimate-result">
                                                        <FaCheckCircle color="#4caf50" />
                                                        <span>Legitimate</span>
                                                        <span className="confidence">
                                                            ({Math.round(item.confidence * 100)}%)
                                                        </span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="email-history">
                            <h2>Email Check History</h2>

                            {emailHistory.length === 0 ? (
                                <div className="no-history">No email check history available</div>
                            ) : (
                                <div className="history-list">
                                    {emailHistory.map((item) => (
                                        <div key={item.id} className="history-item">
                                            <div className="history-item-content">
                                                <div className="history-subject">
                                                    <strong>Subject:</strong> {truncate(item.subject) || '(No subject)'}
                                                </div>
                                                <div className="history-sender">
                                                    <strong>From:</strong> {truncate(item.sender) || '(Unknown sender)'}
                                                </div>
                                                <div className="history-date">{formatDate(item.checked_at)}</div>
                                            </div>
                                            <div className="history-result">
                                                {item.is_phishing ? (
                                                    <div className="phishing-result">
                                                        <FaExclamationTriangle color="#f44336" />
                                                        <span>Phishing</span>
                                                        <span className="confidence">
                                                            ({Math.round(item.confidence * 100)}%)
                                                        </span>
                                                    </div>
                                                ) : (
                                                    <div className="legitimate-result">
                                                        <FaCheckCircle color="#4caf50" />
                                                        <span>Legitimate</span>
                                                        <span className="confidence">
                                                            ({Math.round(item.confidence * 100)}%)
                                                        </span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default History;