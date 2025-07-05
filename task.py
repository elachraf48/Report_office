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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
def login_if_needed(email, password):
    profile_path = os.path.join(PROFILE_DIR, email)

    options = Options()
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
        driver.get("https://outlook.office.com/mail/")
        time.sleep(5)

        if "login.microsoftonline.com" in driver.current_url or "www.microsoft.com" in driver.current_url:
            print(f"[!] Profile {email} is not logged in. Logging in now...")

            driver.get(LOGIN_URL)
            time.sleep(3)

            # ✅ Handle "Choose an account" screen
            try:
                account_list = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="accountTile"]')
                matched = False
                for account in account_list:
                    if email in account.text:
                        account.click()
                        matched = True
                        print(f"[✓] Selected existing account: {email}")
                        break

                if not matched:
                    print("[~] Email not listed, selecting 'Use another account'")
                    other_account = driver.find_element(By.XPATH, "//div[contains(text(), 'Utiliser un autre compte')]")
                    other_account.click()
                    time.sleep(2)

            except Exception as e:
                print("[~] No account selection screen, proceeding directly")

            # ✅ Now do login steps
            try:
                email_input = driver.find_element(By.NAME, "loginfmt")
                email_input.clear()
                email_input.send_keys(email)
                email_input.send_keys(Keys.ENTER)
                time.sleep(3)
            except:
                pass  # Already selected

            try:
                password_input = driver.find_element(By.NAME, "passwd")
                password_input.clear()
                password_input.send_keys(password)
                password_input.send_keys(Keys.ENTER)
                time.sleep(3)
            except:
                print("[~] Password input not found, maybe already authenticated")

            try:
                driver.find_element(By.ID, "idBtn_Back").click()  # No button
            except:
                pass

            time.sleep(5)
            print(f"[+] Login success: {email}")

        return driver

    except Exception as e:
        print(f"[!] Error during login for {email}: {e}")
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_email = email.replace('@', '_at_').replace('.', '_')
            screenshot_path = os.path.join(ERRORS_DIR, f"{safe_email}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"[!] Screenshot saved: {screenshot_path}")
        except:
            print("[!] Failed to save screenshot.")
        if 'driver' in locals():
            driver.quit()
        return None


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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def task_report_not_junk(driver):
    print("🚫 Trying to report as not junk...")

    try:
        driver.get("https://outlook.office.com/mail/junkemail")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message list"]'))
        )
        time.sleep(3)

        # Get list of junk emails
        emails = driver.find_elements(By.XPATH, '//div[@aria-label="Message list"]//div[@role="option"]')

        if not emails:
            print("📭 No emails found in Junk folder.")
            return

        print(f"[✓] Found {len(emails)} email(s) in junk.")

        first_email = emails[0]
        first_email_text = first_email.text.strip()

        first_email.click()
        print("📨 Opened first junk email")
        time.sleep(6)

        # After clicking, go back to junk folder and check if email disappeared
        driver.get("https://outlook.office.com/mail/junkemail")
        time.sleep(5)

        new_emails = driver.find_elements(By.XPATH, '//div[@aria-label="Message list"]//div[@role="option"]')
        email_titles = [e.text.strip() for e in new_emails]

        if first_email_text not in email_titles:
            print("✅ Email marked as not junk (automatically moved)")
        else:
            print("⚠️ Email still in junk — no automatic move detected")

    except Exception as e:
        print(f"[!] Error while reporting not junk: {e}")





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