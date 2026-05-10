import pytest


pytestmark = pytest.mark.lifecycle

def test_move_folder(client, unique_folder_name, created_folders):
    source_folder = f"{unique_folder_name}_source"
    moved_folder = f"{unique_folder_name}_moved"

    create_response = client.create_folder(source_folder)
    assert create_response.status_code == 201

    move_response = client.move_resource(
        from_path=source_folder,
        to_path=moved_folder
    )

    assert move_response.status_code in [201, 202]

    old_metadata_response = client.get_resource_metadata(source_folder)
    new_metadata_response = client.get_resource_metadata(moved_folder)
    body = new_metadata_response.json()

    created_folders.append(moved_folder)

    assert old_metadata_response.status_code == 404
    assert new_metadata_response.status_code == 200
    assert body["name"] == moved_folder
    assert body["type"] == "dir"