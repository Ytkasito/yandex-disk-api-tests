import pytest


pytestmark = pytest.mark.crud

def test_get_created_folder_metadata(client, unique_folder_name, created_folders):
    client.create_folder(unique_folder_name)
    created_folders.append(unique_folder_name)

    response = client.get_resource_metadata(unique_folder_name)
    body = response.json()

    assert response.status_code == 200
    assert body["name"] == unique_folder_name
    assert body["type"] == "dir"
    assert body["path"] == f"disk:/{unique_folder_name}"