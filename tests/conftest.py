import uuid

import pytest

from utils.client import YandexDiskClient


@pytest.fixture(scope="session")
def client():
    """Shared client instance for the test session."""
    return YandexDiskClient()


@pytest.fixture
def unique_folder_name():
    return f"test_folder_{uuid.uuid4().hex}"


@pytest.fixture
def unique_file_name():
    return f"test_file_{uuid.uuid4().hex}.txt"


@pytest.fixture
def created_folders(client):
    """Yields a list to which tests can append folder paths for automatic cleanup."""
    folders = []

    yield folders

    for folder in reversed(folders):
        try:
            client.delete_resource(folder, permanently=True)
        except Exception as e:
            # Don't let cleanup errors fail the test run
            import warnings

            warnings.warn(f"Cleanup failed for folder '{folder}': {e}")


@pytest.fixture
def created_files(client):
    """Yields a list to which tests can append file paths for automatic cleanup."""
    files = []

    yield files

    for file_path in reversed(files):
        try:
            client.delete_resource(file_path, permanently=True)
        except Exception as e:
            import warnings

            warnings.warn(f"Cleanup failed for file '{file_path}': {e}")


@pytest.fixture
def existing_folder(client, unique_folder_name, created_folders):
    """Creates a folder before the test and schedules it for cleanup after."""
    response = client.create_folder(unique_folder_name)
    assert response.status_code == 201, (
        f"Setup failed: could not create folder '{unique_folder_name}'. "
        f"Status: {response.status_code}, Body: {response.text}"
    )
    created_folders.append(unique_folder_name)
    return unique_folder_name
