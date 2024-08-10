from dotenv import dotenv_values

# Load environment variables from .env file
env = dotenv_values()

# Define configuration variables
AWB_FILE_PATH = env.get("AWB_FILE_PATH", None)
PREFIX = env.get("PREFIX")
TRACK_URL = env.get("TRACK_URL")
OUTPUT_FILE_PATH = env.get("OUTPUT_FILE_PATH")
OUTPUT_FILE_FORMAT = env.get("OUTPUT_FILE_FORMAT")
