import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auth import create_and_login  # Your login function, must be imported

CHROMEDRIVER_PATH = './drive/chromedriver.exe'
WHITELIST_FILE = 'data/whitelist.txt'
ERRORS_DIR = 'errors'
PROFILE_DIR = 'profiles'

def login_if_needed(profile_name, email, password):
    profile_path = os.path.join(PROFILE_DIR, profile_name)

    options = Options()
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get("https://outlook.live.com/mail/inbox")
    time.sleep(5)

    # If login page detected, login
    if "login.microsoftonline.com" in driver.current_url or "www.microsoft.com" in driver.current_url:
        print(f"[!] Profile {profile_name} is not logged in. Logging in now...")
        driver.quit()
        create_and_login(profile_name, email, password)
        time.sleep(3)

        # reopen after login
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
        driver.get("https://outlook.live.com/mail/inbox")
        time.sleep(5)

    return driver


# task functions (same as you have)
def task_open_inbox(driver):
    print("📥 Opening inbox...")
    driver.get("https://outlook.live.com/mail/inbox")
    time.sleep(10)

def task_report_not_junk(driver):
    print("🚫 Trying to report as not junk...")
    # ... your implementation ...

def task_add_whitelist(driver):
    print("📜 Whitelisting emails (placeholder)")
    # ... your implementation ...

def task_delete_all(driver):
    print("🗑️ Deleting all emails...")
    # ... your implementation ...

def task_delete_n(driver, count):
    print(f"🗑️ Deleting {count} emails...")
    # ... your implementation ...

def task_read_random_n(driver, count):
    print(f"📖 Reading {count} random emails...")
    # ... your implementation ...


def perform_tasks(driver, profile_name, selected_tasks):
    try:
        for task_id in selected_tasks:
            if task_id == "1":
                task_open_inbox(driver)
            elif task_id == "2":
                task_report_not_junk(driver)
            elif task_id == "3":
                task_add_whitelist(driver)
            elif task_id == "4":
                task_delete_all(driver)
            elif task_id == "5":
                count = random.randint(1, 10)
                task_delete_n(driver, count)
            elif task_id == "6":
                count = random.randint(1, 5)
                task_read_random_n(driver, count)

        time.sleep(2)
        driver.quit()

    except Exception as e:
        print(f"[!] Error running tasks in {profile_name}: {e}")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot = os.path.join(ERRORS_DIR, f"{profile_name}_{timestamp}.png")
        try:
            driver.save_screenshot(screenshot)
            print(f"🖼️ Screenshot saved: {screenshot}")
        except:
            print("Failed to save screenshot")
        if 'driver' in locals():
            driver.quit()
