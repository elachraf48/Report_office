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
from selenium.webdriver.common.action_chains import ActionChains    
import traceback

# ========== CONFIGURATION ==========

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
def task_report_not_junk(driver):
    print("🚫 Starting not junk reporting process...")
    
    try:
        # Navigate to junk folder with multiple retries
        print("🌐 Navigating to junk folder...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                driver.get("https://outlook.office.com/mail/junkemail")
                WebDriverWait(driver, 15).until(
                    lambda d: "junkemail" in d.current_url
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"⚠️ Failed to load junk folder after {max_retries} attempts: {e}")
                    raise
                print(f"🔄 Retrying junk folder loading ({attempt + 1}/{max_retries})...")
                time.sleep(2)

        # Wait for page to stabilize
        time.sleep(3)

        # Process all emails in a loop
        processed_count = 0
        while True:
            # Check for empty folder
            empty_indicators = [
                '//*[contains(text(), "aucun message") or contains(text(), "no messages") or contains(text(), "vide")]',
                '//*[contains(text(), "folder is empty")]',
                '//*[contains(@data-automation-id, "emptyFolder")]',
                '//div[contains(@class, "emptyFolder")]'
            ]

            empty_folder = False
            for indicator in empty_indicators:
                try:
                    empty_elements = driver.find_elements(By.XPATH, indicator)
                    if empty_elements and empty_elements[0].is_displayed():
                        print("📭 Junk folder appears to be empty")
                        empty_folder = True
                        break
                except Exception:
                    continue
            
            if empty_folder:
                break

            # Find emails
            email_locators = [
                '//div[@aria-label="Message list"]//div[@role="option"][.//div[@data-automationid="messageListItem"]]',
                '//div[@aria-label="Message list"]//div[contains(@class, "ListItem") and @role="option"]',
                '//div[@data-convid][@role="option"]',
                '//div[contains(@class, "ms-List-cell")][@role="option"]'
            ]

            emails = []
            for locator in email_locators:
                try:
                    emails = driver.find_elements(By.XPATH, locator)
                    if emails:
                        break
                except Exception:
                    continue

            if not emails:
                print("🔍 No emails detected - trying scroll and refresh...")
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(2)
                    refresh_button = driver.find_element(By.XPATH, '//button[@aria-label="Refresh"]')
                    refresh_button.click()
                    time.sleep(3)
                    continue
                except Exception:
                    print("❌ Could not refresh emails list")
                    break

            print(f"📨 Found {len(emails)} email(s) in junk folder")

            # Process first email in the list
            try:
                first_email = emails[0]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_email)
                driver.execute_script("arguments[0].style.border='3px solid red';", first_email)
                time.sleep(1)
                
                # Try multiple click methods
                clicked = False
                try:
                    first_email.click()
                    clicked = True
                except Exception:
                    try:
                        driver.execute_script("arguments[0].click();", first_email)
                        clicked = True
                    except Exception:
                        try:
                            ActionChains(driver).move_to_element(first_email).pause(0.5).click().perform()
                            clicked = True
                        except Exception:
                            pass

                if not clicked:
                    print("❌ Failed to select email")
                    break
                    
                print("✅ Successfully selected email")
                time.sleep(2)

                # Click Not Junk button
                not_junk_xpaths = [
                    '//*[@id="ItemReadingPaneContainer"]/div[2]/div/div[1]/div/div/div[1]/div[3]/div/div/div[3]/button',
                    '//button[contains(@aria-label, "Not junk")]',
                    '//button[contains(@aria-label, "Non indésirable")]',
                    '//button[@name="Not junk"]'
                ]
                
                clicked = False
                for xpath in not_junk_xpaths:
                    try:
                        button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        driver.execute_script("arguments[0].click();", button)
                        print(f"✅ Clicked Not Junk ({xpath[:30]}...)")
                        clicked = True
                        break
                    except Exception:
                        continue

                if not clicked:
                    print("❌ Could not find Not Junk button")
                    break

                # Confirm dialog
                try:
                    confirm_button = WebDriverWait(driver, 7).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[last()]/div[2]/div/div[3]/button[1]'))
                    )
                    driver.execute_script("arguments[0].click();", confirm_button)
                    print("✅ Email marked as not junk")
                    processed_count += 1
                except Exception as e:
                    print(f"⚠️ Confirmation failed: {e}")

                # Short delay before next email
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Error processing email: {e}")
                continue

        print(f"✔️ Process completed. Marked {processed_count} emails as not junk")
        return True

    except Exception as e:
        print(f"❗ Critical error: {str(e)}")
        traceback.print_exc()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"errors/junk_report_fail_{timestamp}.png")
        return False

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