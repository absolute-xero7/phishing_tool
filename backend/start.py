import os
import time
import subprocess
import sys

# First, run the wait_for_db.py script
print("Waiting for database to be ready...")
wait_result = subprocess.run(["python", "wait_for_db.py"], check=False)

if wait_result.returncode != 0:
    print("Failed to connect to the database. Exiting.")
    sys.exit(1)

# Then initialize the database
print("Initializing database...")
init_result = subprocess.run(["python", "init_db.py"], check=False)

if init_result.returncode != 0:
    print("Failed to initialize the database. Exiting.")
    sys.exit(2)

# Finally, start the application
print("Starting application...")
app_result = subprocess.run(["python", "simple_app.py"], check=False)

# Exit with the same code as the application
sys.exit(app_result.returncode)