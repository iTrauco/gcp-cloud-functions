import pytest
from click.testing import CliRunner
from gcp_cli_tool.cli import cli

runner = CliRunner()

# Test deploy_metadata_change command
def test_deploy_metadata_change():
    result = runner.invoke(cli, ['deploy_metadata_change', 'my_bucket'])
    assert result.exit_code == 0
    assert 'Deploying metadata_change function' in result.output

# Test invoke_command
def test_invoke_command():
    result = runner.invoke(cli, ['invoke_command', 'my_function', '--data', 'test_data'])
    assert result.exit_code == 0
    assert 'Invoking function' in result.output

# Test delete_command
def test_delete_command():
    result = runner.invoke(cli, ['delete_command', 'my_function'])
    assert result.exit_code == 0
    assert 'Deleting function' in result.output

# Test auth command
def test_auth():
    result = runner.invoke(cli, ['auth'])
    assert result.exit_code == 0
    assert 'Authenticating with gcloud' in result.output

# Test test_command (assuming you have appropriate mock functions or fixtures for testing)
@pytest.mark.skip(reason="Not yet implemented or requires mock setup")
def test_test_command():
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
    assert 'Testing function' in result.output

