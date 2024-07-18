import os
import json
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def get_chrome_profiles():
    profiles = []
    chrome_path = Path.home() / ".config" / "google-chrome"
    if chrome_path.exists():
        for profile in chrome_path.iterdir():
            if profile.is_dir() and profile.name.startswith("Profile "):
                profiles.append(profile.name)
    return profiles

def get_profile_users():
    profile_users = {}
    chrome_path = Path.home() / ".config" / "google-chrome"
    if chrome_path.exists():
        for profile in get_chrome_profiles():
            preferences_path = chrome_path / profile / "Preferences"
            if preferences_path.exists():
                user_email = extract_user_email(preferences_path)
                if user_email:
                    profile_users[profile] = user_email
    return profile_users

def extract_user_email(preferences_path):
    try:
        with open(preferences_path, "r") as file:
            data = json.load(file)
            email = data.get("account_info", [{}])[0].get("email", None)
            return email
    except (json.JSONDecodeError, KeyError) as e:
        console.print(f"Error reading JSON from Preferences file: {e}", style="bold red")
    return None

def select_chrome_profile():
    profile_users = get_profile_users()
    if not profile_users:
        console.print("No Chrome profiles found.")
        return None, None

    console.print("Select a Chrome profile to use for authentication:")
    for idx, (profile, user) in enumerate(profile_users.items(), 1):
        console.print(f"{idx}. {profile} ({user})")
    console.print(f"{len(profile_users) + 1}. Login to a new account")

    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(profile_users):
                selected_profile = list(profile_users.keys())[choice - 1]
                return selected_profile, profile_users[selected_profile]
            elif choice == len(profile_users) + 1:
                console.print("Opening Chrome for new account login...")
                subprocess.run(["/usr/bin/google-chrome", "--profile-directory=Default", "chrome://settings/people"], check=True)
                
                # Wait for user to login and create new profile
                console.print("Please log into Chrome with your new account. Press Enter when done.")
                input()

                # Refresh profile list and return new profile
                new_profile_users = get_profile_users()
                new_profiles = set(new_profile_users.keys()) - set(profile_users.keys())
                if new_profiles:
                    new_profile = new_profiles.pop()
                    return new_profile, new_profile_users[new_profile]
                else:
                    console.print("No new profile detected. Please try again.")
                    return None, None
            else:
                console.print("Invalid choice. Please enter a valid number.")
        except ValueError:
            console.print("Invalid input. Please enter a number.")
