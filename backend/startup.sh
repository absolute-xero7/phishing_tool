#!/bin/bash

# Wait for database
echo "Waiting for database..."
until PGPASSWORD=postgres psql -h db -U postgres -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up - executing application"

# Run initialization script
python init_db.py

# Start the application
python simple_app.py