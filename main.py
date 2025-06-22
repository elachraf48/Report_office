import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

from task import show_tasks, perform_tasks
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
    updated_lines = []
    profile_index = get_next_profile_number()

    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            email, password = parts
            profile_name = f"office{profile_index}"
            profile_index += 1
            accounts.append((profile_name, email, password))
            updated_lines.append(f"{profile_name}:{email}:{password}")
        elif len(parts) == 3:
            profile_name, email, password = parts
            accounts.append((profile_name, email, password))
            updated_lines.append(line)
        else:
            print(f"[!] Invalid line skipped: {line}")

    if lines != updated_lines:
        with open(DATA_FILE, 'w') as f:
            f.write('\n'.join(updated_lines))
        print("[✓] Updated data.txt with profile names")

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

    for i, (profile_name, email, password) in enumerate(accounts[start_idx:end_idx], start=start_idx + 1):
        print(f"\n[→] Working on profile {i}: {profile_name}")
        profile_path = os.path.join(PROFILE_DIR, profile_name)

        if not os.path.exists(profile_path):
            print(f"[+] Creating and logging in: {profile_name}")
            create_and_login(profile_name, email, password)
        else:
            print(f"[✓] Profile exists: {profile_name}")

        perform_tasks(profile_name, email, password, selected_tasks)


def main():
    print("=== MAIN MENU ===")
    print("1. Create profile(s)")
    print("2. Start repo (task runner)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        accounts = load_accounts()
        for profile_name, email, password in accounts:
            if not os.path.exists(os.path.join(PROFILE_DIR, profile_name)):
                print(f"[~] Creating: {profile_name}")
                create_and_login(profile_name, email, password)
            else:
                print(f"[✓] Already exists: {profile_name}")
    elif choice == '2':
        start_tasks()
    else:
        print("[!] Invalid choice")


if __name__ == "__main__":
    main()
