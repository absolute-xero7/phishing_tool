FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install PostgreSQL client for the health check
RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Command to run when container starts - inline instead of using startup.sh
CMD bash -c "\
    echo 'Waiting for database...' && \
    until PGPASSWORD=postgres psql -h db -U postgres -c '\q'; do \
    echo 'PostgreSQL is unavailable - sleeping'; \
    sleep 1; \
    done && \
    echo 'PostgreSQL is up - executing application' && \
    python init_db.py && \
    python simple_app.py"