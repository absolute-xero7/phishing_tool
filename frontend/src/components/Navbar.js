import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
    FaShieldAlt,
    FaTachometerAlt,
    FaLink,
    FaEnvelope,
    FaHistory,
    FaInfoCircle
} from 'react-icons/fa';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'nav-item active' : 'nav-item';
    };

    return (
        <div className="navbar">
            <div className="navbar-brand">
                <FaShieldAlt size={24} />
                <span className="navbar-logo">Phishing Detector</span>
            </div>
            <div className="navbar-nav">
                <Link to="/" className={isActive('/')}>
                    <FaTachometerAlt className="nav-icon" size={18} />
                    <span className="nav-text">Dashboard</span>
                </Link>
                <Link to="/url-checker" className={isActive('/url-checker')}>
                    <FaLink className="nav-icon" size={18} />
                    <span className="nav-text">URL Checker</span>
                </Link>
                <Link to="/email-checker" className={isActive('/email-checker')}>
                    <FaEnvelope className="nav-icon" size={18} />
                    <span className="nav-text">Email Checker</span>
                </Link>
                <Link to="/history" className={isActive('/history')}>
                    <FaHistory className="nav-icon" size={18} />
                    <span className="nav-text">History</span>
                </Link>
                <Link to="/about" className={isActive('/about')}>
                    <FaInfoCircle className="nav-icon" size={18} />
                    <span className="nav-text">About</span>
                </Link>
            </div>
        </div>
    );
};

export default Navbar;