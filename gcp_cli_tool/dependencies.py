import os
import subprocess
import sys
import click
import pytest
from rich.console import Console

console = Console()

def check_command(command):
    """Check if a command is available on the system."""
    result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def install_package(package_name):
    """Install a Python package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def install_gcloud():
    """Install Google Cloud SDK."""
    if sys.platform == 'linux' or sys.platform == 'darwin':
        url = "https://sdk.cloud.google.com"
        install_script = "curl -sSL {} | bash".format(url)
    elif sys.platform == 'win32':
        url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
        install_script = f"start /wait {url}"
    else:
        raise Exception("Unsupported OS")

    subprocess.check_call(install_script, shell=True)
    console.print("Google Cloud SDK installed successfully. :cloud:", style="bold green")
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/google-cloud-sdk/bin")

def check_and_install_dependencies():
    """Check for required dependencies and install them if missing."""
    required_commands = ['gcloud', 'python3']
    required_packages = ['click', 'google-cloud-functions', 'google-cloud-storage', 'google-auth', 'rich']

    for command in required_commands:
        if not check_command(command):
            console.print(f"{command} not found.", style="bold red")
            if command == 'gcloud':
                console.print("Installing Google Cloud SDK... :cloud:", style="bold green")
                install_gcloud()
            else:
                console.print(f"Please install {command} and try again.", style="bold red")
                sys.exit(1)

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            console.print(f"{package} not found. Installing... :package:", style="bold yellow")
            install_package(package)

    console.print("All dependencies are installed. :white_check_mark:", style="bold green")

def authenticate_gcloud():
    """Prompt the user to authenticate with gcloud if not already authenticated."""
    try:
        result = subprocess.run(["gcloud", "auth", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "No credentialed accounts." in result.stdout.decode('utf-8'):
            subprocess.check_call(["gcloud", "auth", "login"])
            subprocess.check_call(["gcloud", "auth", "application-default", "login"])
        else:
            console.print("Already authenticated. :white_check_mark:", style="bold green")
    except subprocess.CalledProcessError as e:
        console.print("Failed to authenticate. Please try again.", style="bold red")
        sys.exit(1)

def select_or_create_project():
    """Prompt the user to select or create a GCP project if not already set."""
    try:
        result = subprocess.run(["gcloud", "config", "get-value", "project"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout.decode('utf-8').strip():
            console.print(f"Current project: {result.stdout.decode('utf-8').strip()} :white_check_mark:", style="bold green")
        else:
            console.print("No project set. :warning:", style="bold yellow")
            set_project()
    except subprocess.CalledProcessError as e:
        console.print("Failed to get current project. Please try again.", style="bold red")
        sys.exit(1)

def set_project():
    """Prompt the user to select or create a GCP project."""
    projects = subprocess.check_output(["gcloud", "projects", "list", "--format", "value(projectId)"])
    projects = projects.decode("utf-8").split()

    if projects:
        console.print("Select a project from the list:", style="bold blue")
        for i, project in enumerate(projects, 1):
            console.print(f"{i}. {project}")

        choice = click.prompt("Enter the number of the project to select or 'n' to create a new project", type=str)
        if choice.lower() == 'n':
            project_id = click.prompt("Enter the new project ID")
            subprocess.check_call(["gcloud", "projects", "create", project_id])
            subprocess.check_call(["gcloud", "config", "set", "project", project_id])
        else:
            project_id = projects[int(choice) - 1]
            subprocess.check_call(["gcloud", "config", "set", "project", project_id])
    else:
        console.print("No existing projects found. Creating a new project. :warning:", style="bold yellow")
        project_id = click.prompt("Enter the new project ID")
        subprocess.check_call(["gcloud", "projects", "create", project_id])
        subprocess.check_call(["gcloud", "config", "set", "project", project_id])

    console.print(f"Using project: {project_id} :white_check_mark:", style="bold green")

if __name__ == "__main__":
    check_and_install_dependencies()
    authenticate_gcloud()
    select_or_create_project()
