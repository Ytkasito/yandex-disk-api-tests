import uuid

import pytest

from utils.client import YandexDiskClient


@pytest.fixture
def client():
    return YandexDiskClient()


@pytest.fixture
def unique_folder_name():
    return f"test_folder_{uuid.uuid4().hex}"


@pytest.fixture
def unique_file_name():
    return f"test_file_{uuid.uuid4().hex}.txt"


@pytest.fixture
def created_folders(client):
    folders = []

    yield folders

    for folder in folders:
        client.delete_resource(folder, permanently=True)


@pytest.fixture
def created_files(client):
    files = []

    yield files

    for file_path in files:
        client.delete_resource(file_path, permanently=True)
