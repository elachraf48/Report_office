# task.py

import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auth import create_and_login
import datetime

CHROMEDRIVER_PATH = './drive/chromedriver.exe'
WHITELIST_FILE = 'data/whitelist.txt'
ERRORS_DIR = 'errors'
PROFILE_DIR = 'profiles'
LOGIN_URL = 'https://login.microsoftonline.com/'


def show_tasks():
    tasks = {
        "1": "Open inbox",
        "2": "Report not junk",
        "3": "Add to whitelist",
        "4": "Delete all emails",
        "5": "Delete +N emails",
        "6": "Read random +N emails"
    }
    print("Available tasks:")
    for k, v in tasks.items():
        print(f"{k}. {v}")
    choice = input("Select tasks (e.g. 1+3+5): ").split('+')
    return choice


# ========== TASK IMPLEMENTATIONS ==========


def login_if_needed(profile_name, email, password):
    profile_path = os.path.join(PROFILE_DIR, profile_name)

    options = Options()
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get("https://outlook.office.com/mail/")
    time.sleep(5)

    # If login page detected, login
    if "login.microsoftonline.com" in driver.current_url or "www.microsoft.com" in driver.current_url:
        print(f"[!] Profile {profile_name} is not logged in. Logging in now...")
        try:
            driver.get(LOGIN_URL)
            time.sleep(3)

            email_input = driver.find_element(By.NAME, "loginfmt")
            email_input.clear()
            email_input.send_keys(email)
            email_input.send_keys(Keys.ENTER)
            time.sleep(3)

            password_input = driver.find_element(By.NAME, "passwd")
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(3)

            try:
                driver.find_element(By.ID, "idBtn_Back").click()
            except:
                pass

            time.sleep(5)
            print(f"[+] Login success: {email}")
            

        except Exception as e:
            print(f"[!] Error in {profile_name}: {e}")
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(ERRORS_DIR, f"{profile_name}_{timestamp}.png")
                driver.save_screenshot(screenshot_path)
                print(f"[!] Screenshot saved: {screenshot_path}")
            except:
                print("[!] Failed to save screenshot.")
            if 'driver' in locals():
                driver.quit()
        time.sleep(3)

        # # reopen after login
        # driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
        # driver.get("https://outlook.office.com/mail/")
        # time.sleep(5)

    return driver


# task functions (same as you have)
def task_open_inbox(driver):
    print("📥 Opening inbox...")
    driver.get("https://outlook.office.com/mail/")
    time.sleep(10)

def task_open_junk(driver):
    print("📂 Opening junk folder...")
    try:
        driver.get("https://outlook.office.com/mail/junkemail")
        time.sleep(50)  # Wait for junk folder to load
    except Exception as e:
        print(f"[!] Failed to open junk folder: {e}")

def task_report_not_junk(driver):
    print("🚫 Trying to report as not junk...")

    try:
        driver.get("https://outlook.office.com/mail/junkemail")
        time.sleep(7)

        # Find the email list container
        emails = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Message list"] [tabindex]')

        if not emails:
            print("📭 No emails found in Junk folder.")
            return

        # Click the first email
        emails[0].click()
        time.sleep(6)

        # Try to find and click the 'Not junk' button
        not_junk_button = driver.find_element(By.XPATH, '//button[contains(text(),"Not junk")]')
        not_junk_button.click()
        print("✅ Marked as not junk")

    except Exception as e:
        print(f"[!] Failed to report not junk: {e}")



def task_add_whitelist(driver):
    print("📜 Whitelisting emails (placeholder)")
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE) as f:
            whitelist = [line.strip() for line in f if line.strip()]
        print(f"Whitelist entries: {whitelist}")
    else:
        print("⚠️ whitelist.txt not found")


def task_delete_all(driver):
    print("🗑️ Deleting all emails...")
    try:
        select_all = driver.find_element(By.CSS_SELECTOR, '[aria-label="Select all"]')
        select_all.click()
        time.sleep(1)
        delete = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Delete")]')
        delete.click()
        print("✅ All emails deleted")
    except Exception as e:
        print(f"[!] Could not delete all: {e}")


def task_delete_n(driver, count):
    print(f"🗑️ Deleting {count} emails...")
    try:
        emails = driver.find_elements(By.CSS_SELECTOR, '[tabindex]')
        for i in range(min(count, len(emails))):
            emails[i].click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[contains(@aria-label, "Delete")]').click()
            time.sleep(2)
        print("✅ Deleted selected emails")
    except Exception as e:
        print(f"[!] Failed to delete emails: {e}")


def task_read_random_n(driver, count):
    print(f"📖 Reading {count} random emails...")
    try:
        emails = driver.find_elements(By.CSS_SELECTOR, '[tabindex]')
        random.shuffle(emails)
        for i in range(min(count, len(emails))):
            emails[i].click()
            print(f"📬 Opened email #{i+1}")
            time.sleep(3)
            driver.back()
            time.sleep(2)
    except Exception as e:
        print(f"[!] Failed to read emails: {e}")


# ========== MAIN TASK EXECUTION ==========
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