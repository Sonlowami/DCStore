import os

# Path to your environment variables file
env_file_path = '.env'

# Check if the file exists
if os.path.isfile(env_file_path):
    with open(env_file_path, 'r') as file:
        for line in file:
            # Strip leading/trailing whitespace and split the line into key-value pairs
            pair = line.strip().split('=')
            key = pair[0]
            value = pair[1]
            
            # Set the environment variable
            os.environ[key] = value
