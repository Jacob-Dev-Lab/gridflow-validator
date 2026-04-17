import winsound
import logging

from services.email_service import EmailService
from models.validation_result import ValidationResult


class AlertService:

    def __init__(self):
        self.email_service = EmailService()

    def trigger_alert(self, result: ValidationResult):
        """
        Handles mismatch alerts:
        - logs issue
        - prints alert
        - beeps (Windows only)
        - sends email
        """

        if result.is_valid:
            return  # No alert needed

        message = self._build_message(result)

        # Console output
        print(message)
        logging.warning(message)

        # Audible alert (Windows only)
        self._beep_alert()

        # Email alert
        subject = f"[ALERT] Energy Mismatch - {result.hour_label}"
        self.email_service.send_email(subject, message)

    def _build_message(self, result: ValidationResult) -> str:
        return f"""
            ⚠️ ENERGY FLOW MISMATCH DETECTED

            Hour: {result.hour_label}
            Direction: {result.direction}

            CSV Value: {result.csv_value}
            XML Value: {result.xml_value}

            Status: INVALID ❌

            Please investigate immediately.

            Suggested Correct Flow Value: {result.csv_value}
            """

    def _beep_alert(self):
        try:
            for _ in range(3):
                winsound.Beep(2000, 1000)
        except Exception:
            # Non-Windows systems fallback
            pass