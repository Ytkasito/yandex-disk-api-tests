import allure
import pytest
import requests


pytestmark = pytest.mark.negative


@allure.feature("Negative API scenarios")
@allure.story("Create existing folder")
@allure.title("Should return 409 when creating existing folder")
def test_should_return_409_when_creating_existing_folder(
        client,
        unique_folder_name,
        created_folders
):
    with allure.step("Create folder for the first time"):
        first_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

    with allure.step("Try to create folder with the same name"):
        second_response = client.create_folder(unique_folder_name)

    with allure.step("Check conflict response"):
        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert second_response.json()["error"] == "DiskPathPointsToExistentDirectoryError"


@allure.feature("Negative API scenarios")
@allure.story("Get non-existing resource")
@allure.title("Should return 404 for non-existing resource")
def test_should_return_404_for_non_existing_resource(client):
    with allure.step("Get metadata for non-existing resource"):
        response = client.get_resource_metadata("definitely_non_existing_folder")

    with allure.step("Check not found response"):
        assert response.status_code == 404
        assert response.json()["error"] == "DiskNotFoundError"


@allure.feature("Negative API scenarios")
@allure.story("Unauthorized request")
@allure.title("Should return 401 without OAuth token")
def test_should_return_401_without_oauth_token():
    with allure.step("Send request without Authorization header"):
        response = requests.get("https://cloud-api.yandex.net/v1/disk")

    with allure.step("Check unauthorized response"):
        assert response.status_code == 401
        assert response.json()["error"] == "UnauthorizedError"