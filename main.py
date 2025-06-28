import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

from task import show_tasks, perform_tasks, login_if_needed
from auth import create_and_login

# === CONFIG ===
DATA_FILE = 'data/data.txt'
NAME_FILE = 'data/name.txt'
PROFILE_DIR = 'profiles'
ERRORS_DIR = 'errors'
CHROMEDRIVER_PATH = './drive/chromedriver.exe'
LOGIN_URL = 'https://login.microsoftonline.com/'

# === Ensure necessary folders exist ===
os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(ERRORS_DIR, exist_ok=True)

def get_next_profile_number():
    profiles = [d for d in os.listdir(PROFILE_DIR) if d.startswith("office")]
    numbers = [int(d.replace("office", "")) for d in profiles if d.replace("office", "").isdigit()]
    return max(numbers + [0]) + 1

def load_accounts():
    with open(DATA_FILE, 'r') as f:
        lines = [line.strip() for line in f if ':' in line]

    accounts = []
    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            email, password = parts
            accounts.append((email, password))
        else:
            print(f"[!] Skipping invalid line: {line}")
    return accounts



def start_tasks():
    accounts = load_accounts()
    selected_tasks = show_tasks()

    start_input = input("Start from which account? (press Enter to start from 1): ").strip()
    if start_input == "":
        start_idx = 0
        end_idx = len(accounts)
    else:
        try:
            start_idx = int(start_input) - 1
            end_input = input("End at which account? : ").strip()
            end_idx = int(end_input) if end_input else len(accounts)
        except ValueError:
            print("[!] Invalid input, using full list.")
            start_idx = 0
            end_idx = len(accounts)

    for i, (email, password) in enumerate(accounts[start_idx:end_idx], start=start_idx + 1):
        print(f"\n[→] Working on {email}")
        profile_path = os.path.join(PROFILE_DIR, email)

        if not os.path.exists(profile_path):
            print(f"[+] Creating login session for {email}")
            create_and_login(email, password)
        else:
            print(f"[✓] Profile already exists for {email}")

        driver = login_if_needed(email, password)
        if driver is None:
            print(f"[X] Skipping {email} due to login failure.")
            continue  # move to next profile
        perform_tasks(driver, email, selected_tasks)


def main():
    print("=== MAIN MENU ===")
    print("1. Create profiles only")
    print("2. Start tasks")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        accounts = load_accounts()
        for email, password in accounts:
            profile_path = os.path.join(PROFILE_DIR, email)
            if not os.path.exists(profile_path):
                print(f"[~] Creating profile for {email}")
                create_and_login(email, password)
            else:
                print(f"[✓] Profile exists for {email}")
    elif choice == "2":
        start_tasks()
    else:
        print("[!] Invalid choice")


if __name__ == "__main__":
    main()