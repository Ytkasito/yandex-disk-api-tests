import pytest


pytestmark = pytest.mark.crud

from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_create_folder(client, unique_folder_name, created_folders):
    response = client.create_folder(unique_folder_name)
    created_folders.append(unique_folder_name)

    assert response.status_code == 201