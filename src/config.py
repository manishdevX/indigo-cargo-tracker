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
EMAIL_ATTACHMENT_FORMAT = env.get("EMAIL_ATTACHMENT_FORMAT")
EMAIL_HOST = env.get("EMAIL_HOST")
EMAIL_PASSWORD = env.get("EMAIL_PASSWORD")
EMAIL_PORT = env.get("EMAIL_PORT", 587)
SENDER_EMAIL = env.get("SENDER_EMAIL")
RECIPIENT_EMAILS = env.get("RECIPIENT_EMAILS").split(",")
