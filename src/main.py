from __future__ import annotations
import json
from menu import display_menu, handle_menu_selection
from profile import create_profile
from repository import start_repository
from utils.error_logging import log_error

def main():
    while True:
        try:
            display_menu()
            choice = input("Select an option: ")
            if choice == '1':
                create_profile()
            elif choice == '2':
                start_repository()
            elif choice == '3':
                print("Exiting the application.")
                break
            else:
                print("Invalid selection. Please try again.")
        except Exception as e:
            log_error(str(e))

if __name__ == "__main__":
    main()