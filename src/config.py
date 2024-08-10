from dotenv import dotenv_values

# Load environment variables from .env file
env = dotenv_values()

# Define configuration variables
AWB_FILE_PATH = env.get("AWB_FILE_PATH", None)
PREFIX = env.get("PREFIX")
TRACK_URL = env.get("TRACK_URL")
RESULT_STORAGE_ENABLED = env.get("RESULT_STORAGE_ENABLED", "true") == "true"
RESULT_FILE_FORMAT = env.get("RESULT_FILE_FORMAT", "csv")
RESULT_FILE_PATH = env.get("RESULT_FILE_PATH")
RESULT_EMAIL_ENABLED = env.get("RESULT_EMAIL_ENABLED", "false") == "true"
