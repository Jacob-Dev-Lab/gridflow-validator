import os
import time
import pandas as pd
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.config import CSV_DIR
from utils.time_utils import get_london_time
from utils.logger import setup_logger


class RNPScraper:
    def __init__(self):
        self._initialized = False
        self.url = "https://rnp.unicorn.com"
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 60)
        self.logger = setup_logger()

    def _init_driver(self):
        options = Options()
        options.set_preference("detach", True)
        service = Service()
        return webdriver.Firefox(service=service, options=options)

    def open_site(self):
        self.driver.get(self.url)
        print("📡 RNP website loaded")

    def _set_business_day_if_needed(self):
        """
        Switch RNP UI to next trading day if current time >= 21:00
        """

        now = get_london_time()

        if now.hour < 21:
            return  # No action needed

        self.logger.info("Switching to next business day")

        next_day = now + timedelta(days=1)
        next_day_value = next_day.day

        # Click date picker
        business_day_input = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "tradingDay"))
        )
        business_day_input.click()

        try:
            date_cell = self.driver.find_element(
                By.XPATH,
                f"//table/tbody//td[.//div/div[text()='{next_day_value}']]"
            )
        except:
            date_cell = self.driver.find_element(
                By.XPATH,
                f"//table/tbody//td[.//div/div/span[text()='{next_day_value}']]"
            )

        date_cell.click()

        self.logger.info(
            f"Business day set to {next_day.strftime('%d-%m-%Y')}"
        )

    def scrape_table(self):
        """
        Extract table data from RNP page
        """
        # Step 1: Click Public Access
        public_access_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Public')]"))
        )
        public_access_button.click()

        time.sleep(5)

        # Step 2: Click Show Data
        show_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show')]"))
        )
        show_button.click()

        # Step 3: WAIT for table to appear (IMPORTANT FIX)
        self.wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "tbody"))
        )

        time.sleep(5)
        
        tables = self.driver.find_elements(By.TAG_NAME, "tbody")
        if len(tables) < 2:
            raise Exception("Data table not found")

        rows = tables[1].find_elements(By.TAG_NAME, "tr")

        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([c.text for c in cols])

        return data

    def save_to_csv(self, data):
        os.makedirs(CSV_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rnp_{timestamp}.csv"
        filepath = os.path.join(CSV_DIR, filename)

        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, header=False)

        print(f"✅ Saved: {filepath}")
        return filepath

    def run_once(self):
        if not self._initialized:
            self.open_site()
            self._initialized = True

        self.driver.refresh()
        self._set_business_day_if_needed()
        data = self.scrape_table()
        return self.save_to_csv(data)

    def close(self):
        self.driver.quit()