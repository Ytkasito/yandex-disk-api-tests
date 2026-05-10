import allure
import pytest


pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Get resource metadata")
@allure.title("Should return created folder metadata")
def test_get_created_folder_metadata(
        client,
        unique_folder_name,
        created_folders
):
    with allure.step("Create test folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert create_response.status_code == 201

    with allure.step("Get folder metadata"):
        response = client.get_resource_metadata(unique_folder_name)
        body = response.json()

    with allure.step("Validate folder metadata"):
        assert response.status_code == 200
        assert body["name"] == unique_folder_name
        assert body["type"] == "dir"
        assert body["path"] == f"disk:/{unique_folder_name}"