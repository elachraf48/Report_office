import os
import time
import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CHROMEDRIVER_PATH = './drive/chromedriver.exe'
PROFILE_DIR = 'profiles'
ERRORS_DIR = 'errors'
LOGIN_URL = 'https://login.microsoftonline.com/'


def create_and_login(profile_name, email, password):
    profile_path = os.path.join(PROFILE_DIR, profile_name)

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    try:
        driver = uc.Chrome(driver_executable_path=CHROMEDRIVER_PATH, options=options)
        driver.get(LOGIN_URL)
        time.sleep(3)

        email_input = driver.find_element(By.NAME, "loginfmt")
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        time.sleep(3)

        password_input = driver.find_element(By.NAME, "passwd")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)

        try:
            driver.find_element(By.ID, "idBtn_Back").click()
        except:
            pass

        time.sleep(5)
        print(f"[+] Login success: {email}")
        driver.quit()

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
