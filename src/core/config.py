import os
from dotenv import load_dotenv

load_dotenv()

CSV_DIR = "data/csv"
XML_DIR = "data/xml"
LOG_FILE = "logs/app.log"

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value

SMTP_SERVER = get_env_variable("SMTP_SERVER")
SMTP_PORT = int(get_env_variable("SMTP_PORT"))

EMAIL_SENDER = get_env_variable("EMAIL_SENDER")
EMAIL_PASSWORD = get_env_variable("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = get_env_variable("EMAIL_RECIPIENTS").split(",")