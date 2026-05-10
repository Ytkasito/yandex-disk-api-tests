import pytest


pytestmark = pytest.mark.lifecycle

def test_restore_folder_from_trash(client, unique_folder_name, created_folders):
    restored_folder_name = f"{unique_folder_name}_restored"

    create_response = client.create_folder(unique_folder_name)
    assert create_response.status_code == 201

    delete_response = client.delete_resource(
        unique_folder_name,
        permanently=False
    )
    assert delete_response.status_code in [202, 204]

    trash_response = client.get_trash_resource_metadata("/")
    trash_items = trash_response.json()["_embedded"]["items"]

    deleted_folder = next(
        item for item in trash_items
        if item["name"] == unique_folder_name
    )

    restore_response = client.restore_from_trash(
        path=deleted_folder["path"],
        name=restored_folder_name,
        overwrite=True
    )

    assert restore_response.status_code in [201, 202]

    metadata_response = client.get_resource_metadata(restored_folder_name)
    body = metadata_response.json()

    created_folders.append(restored_folder_name)

    assert metadata_response.status_code == 200
    assert body["name"] == restored_folder_name
    assert body["type"] == "dir"