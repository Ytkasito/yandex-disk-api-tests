import pytest


pytestmark = pytest.mark.lifecycle

from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_copy_folder(client, unique_folder_name, created_folders):
    source_folder = f"{unique_folder_name}_source"
    copied_folder = f"{unique_folder_name}_copy"

    client.create_folder(source_folder)
    created_folders.append(source_folder)

    response = client.copy_resource(source_folder, copied_folder)
    created_folders.append(copied_folder)

    assert response.status_code in [201, 202]