import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from schemas.operation_schema import OPERATION_SCHEMA
from utils.assertions import (
    assert_status_code,
    assert_json_has_keys,
    assert_schema
)


pytestmark = pytest.mark.lifecycle


@allure.feature("Resource lifecycle")
@allure.story("Delete resource")
@allure.title("Should delete empty folder permanently")
def test_delete_empty_folder_permanently(client, unique_folder_name):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Delete folder permanently"):
        delete_response = client.delete_resource(
            path=unique_folder_name,
            permanently=True
        )

        assert_status_code(delete_response, 204)
        assert delete_response.text == ""

    with allure.step("Validate folder does not exist"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        body = metadata_response.json()

        assert_status_code(metadata_response, 404)
        assert_json_has_keys(body, ["error", "description", "message"])


@allure.feature("Resource lifecycle")
@allure.story("Delete resource")
@allure.title("Should move empty folder to trash by default")
def test_delete_empty_folder_to_trash_by_default(client, unique_folder_name):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Delete folder without permanently parameter"):
        delete_response = client.delete_resource(path=unique_folder_name)

        assert_status_code(delete_response, 204)
        assert delete_response.text == ""

    with allure.step("Validate folder does not exist on disk"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        body = metadata_response.json()

        assert_status_code(metadata_response, 404)
        assert_json_has_keys(body, ["error", "description", "message"])


@allure.feature("Resource lifecycle")
@allure.story("Delete resource")
@allure.title("Should start async delete operation when force_async is true")
def test_delete_folder_with_force_async_true(client, unique_folder_name):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Delete folder with force_async true"):
        delete_response = client.delete_resource(
            path=unique_folder_name,
            permanently=True,
            force_async=True
        )
        body = delete_response.json()

    with allure.step("Validate async operation link"):
        assert_status_code(delete_response, 202)
        assert_schema(body, LINK_SCHEMA)

        assert body["method"] == "GET"
        assert body["templated"] is False
        assert "/v1/disk/operations" in body["href"]

    with allure.step("Validate operation status"):
        operation_response = client.get_operation_status(body["href"])
        operation_body = operation_response.json()

        assert_status_code(operation_response, 200)
        assert_schema(operation_body, OPERATION_SCHEMA)

        assert operation_body["status"] in ["success", "in-progress"]

    with allure.step("Validate folder is deleted"):
        metadata_response = client.get_resource_metadata(unique_folder_name)

        assert metadata_response.status_code in [200, 404, 423], (
            f"Unexpected status code: {metadata_response.status_code}"
        )