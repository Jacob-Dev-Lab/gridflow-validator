from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os
from datetime import datetime
from core.config import CSV_DIR

def get_driver():
    options = Options()
    options.set_preference("detach", True)
    return webdriver.Firefox(options=options)

def scrape_rnp_data(driver):
    driver.get("https://rnp.unicorn.com/NOM04")

    # TODO: scraping logic here

    data = []  # extracted rows

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(CSV_DIR, f"rnp_{timestamp}.csv")

    pd.DataFrame(data).to_csv(filepath, index=False)

    return filepath