import time
import pytz
import logging
from datetime import datetime, timezone

from integrations.scraper import RNPScraper
from utils.file_utils import get_latest_file
from utils.time_utils import get_hour_index, format_hour_label, should_run_now
from core.config import XML_DIR

from services.validation_service import ValidationService
from services.alert_service import AlertService
from utils.logger import setup_logger

class JobScheduler:

    def __init__(self):
        self.logger = setup_logger()

        self.scraper = RNPScraper()
        self.validator = ValidationService()
        self.alerter = AlertService()

        self.last_execution = None

    def run(self):
        """
        Main scheduler loop
        """
        self.logger.info("Scheduler started")
        print("🚀 Scheduler started...")

        try:
            while True:
                try:
                    if should_run_now():
                        self.execute_job()

                    time.sleep(5)

                except Exception as e:
                    self.logger.error(f"Scheduler loop error: {e}")

        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped manually")
            print("🛑 Scheduler stopped manually")

        finally:
            self.scraper.close()

    def execute_job(self):
        """
        FULL PIPELINE EXECUTION
        """
        now = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
        now_key = time.time()

        # Prevent duplicate execution within same window
        if self.last_execution and (now_key - self.last_execution < 60):
            return

        self.last_execution = now_key
            
        try:
            print(f"\n⏰ Job triggered at {now.strftime('%H:%M:%S')}")
            logging.info("Job triggered")

            # 1. SCRAPE DATA
            csv_file = self.scraper.run_once()

            # 2. FIND XML FILE
            xml_file = get_latest_file(XML_DIR)

            if not xml_file:
                print("🚨 No XML file found")
                return

            # 3. COMPUTE TARGET HOUR
            hour_index = get_hour_index(offset_hours=2)
            hour_label = format_hour_label(hour_index)

            # 4. VALIDATE
            result = self.validator.validate(
                csv_file=csv_file,
                xml_file=xml_file,
                hour_index=hour_index,
                hour_label=hour_label
            )

            # 5. ALERT IF NEEDED
            self.alerter.trigger_alert(result)