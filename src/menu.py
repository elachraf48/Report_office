from profile import create_profile
from repository import start_repository

def display_menu():
    print("Menu:")
    print("1 - Create Profile")
    print("2 - Start Repository")
    print("3 - Exit")

def handle_menu_selection(choice: str):
    if choice == '1':
        create_profile()
    elif choice == '2':
        start_repository()
    elif choice == '3':
        print("Exiting the application.")
        exit()
    else:
        print("Invalid selection. Please try again.")

def main_menu():
    while True:
        try:
            display_menu()
            user_choice = input("Enter your choice (1-3): ")
            handle_menu_selection(user_choice)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_menu()