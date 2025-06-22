import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='data/error_logs.txt',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def log_error(error_message: str, profile_name: str):
    """Logs an error message with a timestamp and profile name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log = f"{timestamp}_{profile_name}.txt"
    error_folder = 'errors'
    
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    
    # Save the error message to a file
    with open(os.path.join(error_folder, error_log), 'w') as file:
        file.write(error_message)
    
    # Log the error message
    logging.error(f"{profile_name}: {error_message}")