import time
import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def wait_for_db():
    """Wait for the database to be ready."""
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/phishing_detector')
    
    print("Waiting for database to be ready...")
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            # Try to connect to the database
            engine = create_engine(database_url)
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            return True
        except OperationalError as e:
            print(f"Database not ready yet (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_interval)
    
    print("Failed to connect to the database. Exiting.")
    return False

if __name__ == "__main__":
    if wait_for_db():
        print("Database connection successful.")
    else:
        exit(1)