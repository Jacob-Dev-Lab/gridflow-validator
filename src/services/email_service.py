import logging
import smtplib
from email.mime.text import MIMEText
from core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENTS
)


class EmailService:

    def send_email(self, subject: str, message: str):
        """
        Sends email using SMTP SSL
        """

        msg = MIMEText(message)
        msg["Subject"] = subject

        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECIPIENTS)

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(
                    EMAIL_SENDER,
                    EMAIL_RECIPIENTS,
                    msg.as_string()
                )

            print("📧 Email sent successfully")

        except Exception as e:
            logging.error(f"Email sending failed: {e}")
            print(f"🚨 Email failed: {e}")