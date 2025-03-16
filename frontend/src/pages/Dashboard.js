import React, { useState, useEffect } from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
import { FaShieldAlt, FaExclamationTriangle, FaCheckCircle, FaChartBar } from 'react-icons/fa';

// Register Chart.js components
Chart.register(...registerables);

const Dashboard = () => {
    const [stats, setStats] = useState({
        urls: { total: 0, phishing: 0, legitimate: 0, phishing_percentage: 0 },
        emails: { total: 0, phishing: 0, legitimate: 0, phishing_percentage: 0 }
    });

    const [urlHistory, setUrlHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsResponse, historyResponse] = await Promise.all([
                    axios.get('/api/stats'),
                    axios.get('/api/url-history?limit=5')
                ]);

                setStats(statsResponse.data);
                setUrlHistory(historyResponse.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch data. Please try again later.');
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Prepare chart data
    const urlPieData = {
        labels: ['Phishing', 'Legitimate'],
        datasets: [
            {
                data: [stats.urls.phishing, stats.urls.legitimate],
                backgroundColor: ['#f44336', '#4caf50'],
                borderColor: ['#c62828', '#2e7d32'],
                borderWidth: 1,
            }
        ]
    };

    const emailPieData = {
        labels: ['Phishing', 'Legitimate'],
        datasets: [
            {
                data: [stats.emails.phishing, stats.emails.legitimate],
                backgroundColor: ['#f44336', '#4caf50'],
                borderColor: ['#c62828', '#2e7d32'],
                borderWidth: 1,
            }
        ]
    };

    // Chart options
    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            },
        },
    };

    if (loading) {
        return <div className="loading">Loading dashboard data...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="dashboard">
            <div className="card">
                <div className="card-title">URL Detection Statistics</div>
                <div className="stats-container">
                    <div className="stat-item">
                        <div className="stat-value">{stats.urls.total}</div>
                        <div className="stat-label">Total URLs</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#f44336' }}>{stats.urls.phishing}</div>
                        <div className="stat-label">Phishing</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#4caf50' }}>{stats.urls.legitimate}</div>
                        <div className="stat-label">Legitimate</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value">{stats.urls.phishing_percentage.toFixed(1)}%</div>
                        <div className="stat-label">Phishing Rate</div>
                    </div>
                </div>
                <div className="chart-container">
                    {stats.urls.total > 0 ? (
                        <Pie data={urlPieData} options={pieOptions} />
                    ) : (
                        <div className="no-data">No URL data available yet</div>
                    )}
                </div>
            </div>

            <div className="card">
                <div className="card-title">Email Detection Statistics</div>
                <div className="stats-container">
                    <div className="stat-item">
                        <div className="stat-value">{stats.emails.total}</div>
                        <div className="stat-label">Total Emails</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#f44336' }}>{stats.emails.phishing}</div>
                        <div className="stat-label">Phishing</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#4caf50' }}>{stats.emails.legitimate}</div>
                        <div className="stat-label">Legitimate</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value">{stats.emails.phishing_percentage.toFixed(1)}%</div>
                        <div className="stat-label">Phishing Rate</div>
                    </div>
                </div>
                <div className="chart-container">
                    {stats.emails.total > 0 ? (
                        <Pie data={emailPieData} options={pieOptions} />
                    ) : (
                        <div className="no-data">No email data available yet</div>
                    )}
                </div>
            </div>

            <div className="card card-full">
                <div className="card-title">Recent URL Checks</div>
                <div className="history-list">
                    {urlHistory.length > 0 ? (
                        urlHistory.map((item) => (
                            <div key={item.id} className="history-item">
                                <div className="history-item-content">
                                    <div className="history-url">{item.url}</div>
                                    <div className="history-date">
                                        {new Date(item.checked_at).toLocaleString()}
                                    </div>
                                </div>
                                <div
                                    className={`history-status ${item.is_phishing ? 'status-phishing' : 'status-legitimate'}`}
                                >
                                    {item.is_phishing ? 'Phishing' : 'Legitimate'}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="no-data">No URL history available yet</div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;