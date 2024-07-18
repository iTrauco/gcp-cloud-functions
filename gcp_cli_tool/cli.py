import click
from rich.console import Console
from commands import deploy, invoke, delete, list_functions, test_function, auth as auth_command
from dependencies import authenticate_gcloud

# Remove any imports related to project selection
# from gcp_cli_tool.commands.project import select_project

console = Console()

@click.group()
def cli():
    """A CLI tool for managing Google Cloud Functions."""
    pass

@cli.command()
@click.argument("bucket_name")
def deploy_metadata_change(bucket_name):
    """Deploy the metadata_change function."""
    deploy.deploy_metadata_change(bucket_name)

@cli.command()
@click.argument("name")
@click.argument("data", required=False)
def invoke(name, data):
    """Invoke a Google Cloud Function."""
    invoke.invoke_function(name, data)

@cli.command()
@click.argument("name")
def delete(name):
    """Delete a Google Cloud Function."""
    delete.delete_function(name)

@cli.command(name='test')
def test_command():
    """Test a Cloud Function from sample_functions."""
    function_dirs = test_function.list_functions()
    if not function_dirs:
        return

    selected_function = test_function.select_function(function_dirs)
    if not selected_function:
        return

    test_function.list_files_in_function(selected_function)

@cli.command()
def auth():
    """Reset gcloud authentication options."""
    auth_command.auth()

@click.group()
def cli():
    """A CLI tool for managing Google Cloud Functions."""
    if not is_gcloud_installed():
        install_gcloud()
        authenticate_gcloud()
    else:
        console.print("gcloud is already installed.", style="bold green")
        authenticate_gcloud()

if __name__ == "__main__":
    cli()
