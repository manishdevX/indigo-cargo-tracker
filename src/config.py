from dotenv import dotenv_values

# Load environment variables from .env file
env = dotenv_values()

# Define configuration variables
AWB_FILE_PATH = env.get("AWB_FILE_PATH", None)
CHUNK_SIZE = env.get("CHUNK_SIZE", 10)
