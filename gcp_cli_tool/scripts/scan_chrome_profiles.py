import os
import json
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

def display_chrome_profiles():
    profile_users = get_profile_users()
    if not profile_users:
        console.print("No Chrome profiles found.")
        return

    console.print("Currently signed-in Chrome profiles:")
    for profile, user in profile_users.items():
        console.print(f"{profile}: {user}")

if __name__ == "__main__":
    display_chrome_profiles()
