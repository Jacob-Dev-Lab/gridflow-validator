import os
from dotenv import load_dotenv

load_dotenv()

CSV_DIR = "data/csv"
XML_DIR = "data/xml"
LOG_FILE = "logs/app.log"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")