import os

import allure
import pytest
import requests

from utils.assertions import (
    assert_status_code,
    assert_error_response,
    assert_field_value,
    assert_response_time,
)

pytestmark = pytest.mark.negative


@allure.feature("Negative API scenarios")
@allure.story("Create existing folder")
@allure.title("Should return 409 when creating existing folder")
def test_should_return_409_when_creating_existing_folder(
    client, unique_folder_name, created_folders
):
    with allure.step("Create folder for the first time"):
        first_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

    with allure.step("Try to create folder with the same name"):
        second_response = client.create_folder(unique_folder_name)
        body = second_response.json()

    with allure.step("Check conflict response"):
        assert_status_code(first_response, 201)
        assert_status_code(second_response, 409)
        assert_error_response(body)
        assert_field_value(body, "error", "DiskPathPointsToExistentDirectoryError")


@allure.feature("Negative API scenarios")
@allure.story("Get non-existing resource")
@allure.title("Should return 404 for non-existing resource")
def test_should_return_404_for_non_existing_resource(client):
    with allure.step("Get metadata for non-existing resource"):
        response = client.get_resource_metadata("definitely_non_existing_folder")
        body = response.json()

    with allure.step("Check not found response"):
        assert_status_code(response, 404)
        assert_error_response(body)
        assert_field_value(body, "error", "DiskNotFoundError")


@allure.feature("Negative API scenarios")
@allure.story("Unauthorized request")
@allure.title("Should return 401 without OAuth token")
def test_should_return_401_without_oauth_token():
    base_url = os.getenv("BASE_URL", "https://cloud-api.yandex.net")

    with allure.step("Send request without Authorization header"):
        response = requests.get(f"{base_url}/v1/disk", timeout=10)
        body = response.json()

    with allure.step("Check unauthorized response"):
        assert_status_code(response, 401)
        assert_error_response(body)
        assert_field_value(body, "error", "UnauthorizedError")


@allure.feature("Negative API scenarios")
@allure.story("Unauthorized request")
@allure.title("Should return 401 with an invalid OAuth token")
def test_should_return_401_with_invalid_oauth_token():
    base_url = os.getenv("BASE_URL", "https://cloud-api.yandex.net")

    with allure.step("Send request with invalid Authorization header"):
        response = requests.get(
            f"{base_url}/v1/disk",
            headers={"Authorization": "OAuth invalid_token_12345"},
            timeout=10,
        )
        body = response.json()

    with allure.step("Check unauthorized response"):
        assert_status_code(response, 401)
        assert_error_response(body)


@allure.feature("Resource negative cases")
@allure.story("Create folder")
@allure.title("Should return 400 when path is missing")
def test_should_return_400_when_create_folder_without_path(client):
    with allure.step("Create folder without path"):
        response = client.create_folder(path="")
        body = response.json()

    with allure.step("Validate bad request response"):
        assert_status_code(response, 400)
        assert_error_response(body)


@allure.feature("Resource negative cases")
@allure.story("Create folder")
@allure.title("Should return 409 when parent folder does not exist")
def test_should_return_409_when_parent_folder_does_not_exist(
    client, unique_folder_name
):
    missing_parent_path = f"{unique_folder_name}/child"

    with allure.step("Create child folder without existing parent"):
        response = client.create_folder(missing_parent_path)
        body = response.json()

    with allure.step("Validate path does not exist response"):
        assert_status_code(response, 409)
        assert_error_response(body)
        assert_field_value(body, "error", "DiskPathDoesntExistsError")


@allure.feature("Resource negative cases")
@allure.story("Delete resource")
@allure.title("Should return 404 when deleting nonexistent resource")
def test_should_return_404_when_deleting_nonexistent_resource(
    client, unique_folder_name
):
    with allure.step("Delete nonexistent resource"):
        response = client.delete_resource(path=unique_folder_name, permanently=True)
        body = response.json()

    with allure.step("Validate not found response"):
        assert_status_code(response, 404)
        assert_error_response(body)


@allure.feature("Resource negative cases")
@allure.story("Delete resource")
@allure.title("Should return 400 when deleting folder with md5 parameter")
def test_should_return_400_when_deleting_folder_with_md5(
    client, existing_folder, created_folders
):
    with allure.step("Try to delete folder with md5"):
        response = client.delete_resource(
            path=existing_folder, md5="fake-md5", permanently=True
        )
        body = response.json()

    with allure.step("Validate bad request response"):
        assert_status_code(response, 400)
        assert_error_response(body)


@allure.feature("Resource negative cases")
@allure.story("Response time")
@allure.title("Disk info endpoint should respond within 5 seconds")
def test_disk_info_response_time(client):
    with allure.step("Request disk info"):
        response = client.get_disk_info()

    with allure.step("Validate response time"):
        assert_status_code(response, 200)
        assert_response_time(response, max_seconds=5.0)
