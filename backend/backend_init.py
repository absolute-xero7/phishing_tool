import os
import sys

def create_init_files():
    """Create __init__.py files in all subdirectories."""
    directories = [
        'api',
        'models',
        'database',
        'ml',
        'ml/data',
        'ml/models',
        'utils'
    ]
    
    for directory in directories:
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        
        # Create __init__.py file
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Initialize package\n')
            print(f"Created file: {init_file}")

if __name__ == "__main__":
    create_init_files()
    print("Initialization complete.")