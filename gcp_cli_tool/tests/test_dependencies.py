# gcp_cli_tool/tests/test_dependencies.py
import subprocess
import sys
import os
from unittest.mock import patch
import pytest # type: ignore

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the functions from dependencies.py
from dependencies import check_command, install_package, install_gcloud, authenticate_gcloud, select_or_create_project, set_project

def test_check_command_exists():
    assert check_command("ls") == True

def test_check_command_not_exists():
    assert check_command("nonexistent_command") == False

@patch('subprocess.run')
def test_install_package(mock_run):
    mock_run.return_value.returncode = 0
    install_package("test_package")
    mock_run.assert_called_once_with([sys.executable, "-m", "pip", "install", "test_package"])

@patch('subprocess.check_call')
@patch('sys.platform', 'linux')
def test_install_gcloud_linux(mock_check_call):
    install_gcloud()
    mock_check_call.assert_called_once()

@patch('subprocess.check_call')
@patch('sys.platform', 'win32')
def test_install_gcloud_windows(mock_check_call):
    install_gcloud()
    mock_check_call.assert_called_once()

@patch('subprocess.run')
def test_authenticate_gcloud_authenticated(mock_run):
    mock_run.return_value.stdout = b'accounts\n'
    authenticate_gcloud()
    assert mock_run.call_count == 1

@patch('subprocess.run')
def test_authenticate_gcloud_not_authenticated(mock_run):
    mock_run.return_value.stdout = b'No credentialed accounts.'
    with patch('subprocess.check_call') as mock_check_call:
        authenticate_gcloud()
        assert mock_check_call.call_count == 2

@patch('subprocess.run')
def test_select_or_create_project_existing_projects(mock_run):
    mock_run.return_value.stdout = b'project1\nproject2\n'
    with patch('click.prompt') as mock_prompt:
        mock_prompt.return_value = '1'
        select_or_create_project()
        assert mock_prompt.call_count == 1

@patch('subprocess.run')
def test_select_or_create_project_no_projects(mock_run):
    mock_run.return_value.stdout = b''
    with patch('click.prompt') as mock_prompt, patch('subprocess.check_call') as mock_check_call:
        mock_prompt.return_value = 'n'
        select_or_create_project()
        assert mock_prompt.call_count == 1
        assert mock_check_call.call_count == 2

if __name__ == "__main__":
    pytest.main()
