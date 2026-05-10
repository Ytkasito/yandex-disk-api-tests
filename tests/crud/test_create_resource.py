import allure
import pytest


pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Create folder")
@allure.title("Should create folder")
def test_create_folder(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

    with allure.step("Check successful creation response"):
        body = response.json()

        assert response.status_code == 201
        assert body["method"] == "GET"
        assert body["templated"] is False
        assert "href" in body