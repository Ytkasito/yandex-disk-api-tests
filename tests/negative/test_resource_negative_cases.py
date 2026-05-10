import allure
import pytest
import requests

from utils.assertions import (
    assert_status_code,
    assert_json_has_keys
)

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


@allure.feature("Resource negative cases")
@allure.story("Get resource metadata")
@allure.title("Should return 404 for nonexistent resource")
def test_get_nonexistent_resource_metadata(client):
    response = client.get_resource_metadata("not_existing_folder_123456789")
    body = response.json()

    assert response.status_code == 404

    assert "error" in body
    assert "description" in body
    assert "message" in body

    assert isinstance(body["error"], str)
    assert isinstance(body["description"], str)
    assert isinstance(body["message"], str)

    assert body["error"] == "DiskNotFoundError"


@allure.feature("Resource negative cases")
@allure.story("Create folder")
@allure.title("Should return 400 when path is missing")
def test_should_return_400_when_create_folder_without_path(client):
    response = client.create_folder(path="")
    body = response.json()

    assert_status_code(response, 400)

    assert_json_has_keys(body, ["error", "description", "message"])

    assert isinstance(body["error"], str)
    assert isinstance(body["description"], str)
    assert isinstance(body["message"], str)


@allure.feature("Resource negative cases")
@allure.story("Create folder")
@allure.title("Should return 409 when parent folder does not exist")
def test_should_return_409_when_parent_folder_does_not_exist(client, unique_folder_name):
    missing_parent_path = f"{unique_folder_name}/child"

    response = client.create_folder(missing_parent_path)
    body = response.json()

    assert_status_code(response, 409)

    assert_json_has_keys(body, ["error", "description", "message"])

    assert body["error"] == "DiskPathDoesntExistsError"

    assert isinstance(body["description"], str)
    assert isinstance(body["message"], str)

@allure.feature("Resource negative cases")
@allure.story("Delete resource")
@allure.title("Should return 404 when deleting nonexistent resource")
def test_should_return_404_when_deleting_nonexistent_resource(client, unique_folder_name):
    response = client.delete_resource(
        path=unique_folder_name,
        permanently=True
    )
    body = response.json()

    assert_status_code(response, 404)

    assert_json_has_keys(body, ["error", "description", "message"])

    assert isinstance(body["error"], str)
    assert isinstance(body["description"], str)
    assert isinstance(body["message"], str)


@allure.feature("Resource negative cases")
@allure.story("Delete resource")
@allure.title("Should return 400 when deleting folder with md5 parameter")
def test_should_return_400_when_deleting_folder_with_md5(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Try to delete folder with md5"):
        response = client.delete_resource(
            path=unique_folder_name,
            md5="fake-md5",
            permanently=True
        )
        body = response.json()

    with allure.step("Validate error response"):
        assert_status_code(response, 400)

        assert_json_has_keys(body, ["error", "description", "message"])

        assert isinstance(body["error"], str)
        assert isinstance(body["description"], str)
        assert isinstance(body["message"], str)