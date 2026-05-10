import allure
import pytest


pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Delete folder")
@allure.title("Should delete folder permanently")
def test_delete_folder(client, unique_folder_name):
    with allure.step("Create test folder"):
        create_response = client.create_folder(unique_folder_name)
        assert create_response.status_code == 201

    with allure.step("Delete folder permanently"):
        delete_response = client.delete_resource(unique_folder_name)

    with allure.step("Check delete response"):
        assert delete_response.status_code in [202, 204]

    with allure.step("Check folder is not available after deletion"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        assert metadata_response.status_code == 404