import time
import winsound
import pytz
import logging
from datetime import datetime, timezone

from integrations.scraper import RNPScraper
from utils.file_utils import get_latest_file
from utils.time_utils import get_hour_index, format_hour_label, should_run_now
from core.config import XML_DIR

from services.validation_service import ValidationService
from services.alert_service import AlertService
from integrations.xml_monitor import DSXMLMonitor
from utils.logger import setup_logger
from utils.file_utils import ensure_dir


class JobScheduler:

    def __init__(self):
        self.logger = setup_logger()

        self.scraper = RNPScraper()
        self.validator = ValidationService()
        self.alerter = AlertService()
        self.monitor = DSXMLMonitor(XML_DIR)

        self.last_execution_key = None

    def run(self):
        ensure_dir(XML_DIR)

        """
        Main scheduler loop
        """
        self.logger.info("Scheduler started")
        print("🚀 Scheduler started...")

        try:
            self.scraper.open_site()

            while True:
                try:
                    now = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
                    local_tz = pytz.timezone("Europe/London") # Define local time zone
                    local_time = now.astimezone(local_tz)  # Convert to local time zone

                    current_hour = local_time.hour # Extracts the current Hour of the day
                    current_offset = local_time.utcoffset() # Extracts the current UTC offset
                    current_execution_key = (current_hour, current_offset)

                    # Check if it's 45 minutes past the hour
                    if current_execution_key != self.last_execution_key and should_run_now():
                        self.execute_job()

                    time.sleep(5)
                    self.last_execution_key = current_execution_key

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

        # 1. SCRAPE DATA
        csv_file = self.scraper.run_once()
            
        try:
            logging.info(f"Validation execution for {now.strftime('%H:%M:%S')} started")

            while True:
                new_files = self.monitor.monitor()
                if new_files:
                    print(f"🆕 New DS file(s) detected: {new_files}")
                    break
                else:
                    winsound.Beep(2000, 3000)  # Beep at 2000 Hz for 3 second
                    print("⏳ Still waiting... No new DS file yet.")
                    time.sleep(60)  # Wait 60 seconds before checking again

            # 2. FIND XML FILE
            xml_file = get_latest_file(XML_DIR)

            if not xml_file:
                print("🚨 No XML file found")
                return

            # 3. TIME LOGIC
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

            self.logger.info(f"Job execution for {now.strftime('%H:%M:%S')} completed")

        except Exception as e:
            self.logger.error(f"Job execution for {now.strftime('%H:%M:%S')} failed: {e}")