FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install PostgreSQL client for the health check
RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the startup script executable
RUN chmod +x startup.sh

EXPOSE 5000

# Use the startup script
CMD ["./startup.sh"]