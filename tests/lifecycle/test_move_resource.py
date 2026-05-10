import allure
import pytest


pytestmark = pytest.mark.lifecycle


@allure.feature("Resource lifecycle")
@allure.story("Move resource")
@allure.title("Should move folder to new location")
def test_move_folder(client, unique_folder_name, created_folders):
    source_folder = f"{unique_folder_name}_source"
    moved_folder = f"{unique_folder_name}_moved"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)

        assert create_response.status_code == 201

    with allure.step("Move folder to new path"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=moved_folder
        )

    with allure.step("Check move response"):
        assert move_response.status_code in [201, 202]

    with allure.step("Verify old folder path does not exist"):
        old_metadata_response = client.get_resource_metadata(
            source_folder
        )

        assert old_metadata_response.status_code == 404

    with allure.step("Verify moved folder exists"):
        new_metadata_response = client.get_resource_metadata(
            moved_folder
        )

        created_folders.append(moved_folder)

        assert new_metadata_response.status_code == 200

        body = new_metadata_response.json()

        assert body["name"] == moved_folder
        assert body["type"] == "dir"