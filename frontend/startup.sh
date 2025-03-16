#!/bin/sh

# Make sure we have all dependencies
echo "Installing dependencies..."
npm install
npm install --save react-router-dom@6.2.1 react-icons@4.3.1 react-chartjs-2@4.0.1 chart.js@3.7.1 axios@0.26.0

# Start the application
echo "Starting React application..."
npm start