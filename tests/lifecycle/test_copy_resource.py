import allure
import pytest


pytestmark = pytest.mark.lifecycle


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title("Should copy folder")
def test_copy_folder(client, unique_folder_name, created_folders):
    source_folder = f"{unique_folder_name}_source"
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)

        assert create_response.status_code == 201

        created_folders.append(source_folder)

    with allure.step("Copy folder"):
        copy_response = client.copy_resource(
            source_folder,
            copied_folder
        )

        created_folders.append(copied_folder)

    with allure.step("Check copy response"):
        assert copy_response.status_code in [201, 202]

    with allure.step("Verify copied folder exists"):
        metadata_response = client.get_resource_metadata(copied_folder)

        assert metadata_response.status_code == 200

        body = metadata_response.json()

        assert body["name"] == copied_folder
        assert body["type"] == "dir"