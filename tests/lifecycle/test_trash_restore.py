import allure
import pytest


pytestmark = pytest.mark.lifecycle


@allure.feature("Resource lifecycle")
@allure.story("Trash restore")
@allure.title("Should restore folder from trash")
def test_restore_folder_from_trash(
        client,
        unique_folder_name,
        created_folders
):
    restored_folder_name = f"{unique_folder_name}_restored"

    with allure.step("Create folder"):
        create_response = client.create_folder(
            unique_folder_name
        )

        assert create_response.status_code == 201

    with allure.step("Move folder to trash"):
        delete_response = client.delete_resource(
            unique_folder_name,
            permanently=False
        )

        assert delete_response.status_code in [202, 204]

    with allure.step("Get deleted folder metadata from trash"):
        trash_response = client.get_trash_resource_metadata("/")

        assert trash_response.status_code == 200

        trash_items = trash_response.json()["_embedded"]["items"]

        deleted_folder = next(
            item for item in trash_items
            if item["name"] == unique_folder_name
        )

    with allure.step("Restore folder from trash"):
        restore_response = client.restore_from_trash(
            path=deleted_folder["path"],
            name=restored_folder_name,
            overwrite=True
        )

        assert restore_response.status_code in [201, 202]

    with allure.step("Verify restored folder exists"):
        metadata_response = client.get_resource_metadata(
            restored_folder_name
        )

        created_folders.append(restored_folder_name)

        assert metadata_response.status_code == 200

        body = metadata_response.json()

        assert body["name"] == restored_folder_name
        assert body["type"] == "dir"