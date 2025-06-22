from typing import Optional
import json
import os
import random
from datetime import datetime

class UserProfile:
    def __init__(self, name: str):
        self.name = name

    def save_to_file(self, filepath: str):
        user_data = {
            "name": self.name
        }
        with open(filepath, 'w') as f:
            json.dump(user_data, f)

def generate_random_name() -> str:
    last_names = []
    office_folder = "office"  # Assuming this folder exists in the current directory
    if os.path.exists(office_folder):
        last_names = [name for name in os.listdir(office_folder) if os.path.isfile(os.path.join(office_folder, name))]
    if last_names:
        return random.choice(last_names).split('.')[0]  # Return the last name without the file extension
    return "DefaultName"

def create_profile(filepath: str, name: Optional[str] = None) -> UserProfile:
    if name is None:
        name = generate_random_name()
    profile = UserProfile(name)
    profile.save_to_file(filepath)
    return profile

def create_multiple_profiles():
    num_profiles = int(input("Enter the number of profiles to create: "))
    base_name = "office"
    profiles = []

    for i in range(num_profiles):
        profile_name = f"{base_name}{i + 1}"
        profiles.append(profile_name)

    # Save profiles to a file
    with open("profiles.txt", "w") as file:
        file.write("\n".join(profiles))
    
    print(f"Created {num_profiles} profiles.")