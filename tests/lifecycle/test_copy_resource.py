import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from utils.assertions import assert_status_code, assert_json_has_keys, assert_schema

import time
from schemas.operation_schema import OPERATION_SCHEMA

pytestmark = pytest.mark.lifecycle


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title("Should copy empty folder and return link body")
def test_copy_empty_folder(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)
        created_folders.append(source_folder)
        created_folders.append(copied_folder)

        assert_status_code(create_response, 201)

    with allure.step("Copy source folder"):
        copy_response = client.copy_resource(
            from_path=source_folder, path=copied_folder
        )
        body = copy_response.json()

    with allure.step("Validate copy response"):
        assert_status_code(copy_response, 201)
        assert_schema(body, LINK_SCHEMA)
        assert_json_has_keys(body, ["href", "method", "templated"])

        assert body["method"] == "GET"
        assert body["templated"] is False
        assert isinstance(body["href"], str)

    with allure.step("Validate copied folder metadata"):
        metadata_response = client.get_resource_metadata(copied_folder)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)

        assert metadata_body["name"] == copied_folder
        assert metadata_body["type"] == "dir"
        assert metadata_body["path"] == f"disk:/{copied_folder}"


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title("Should copy folder with fields filter")
def test_copy_folder_with_fields_filter(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)
        created_folders.append(source_folder)
        created_folders.append(copied_folder)

        assert_status_code(create_response, 201)

    with allure.step("Copy source folder with fields filter"):
        copy_response = client.copy_resource(
            from_path=source_folder, path=copied_folder, fields="href,method"
        )
        body = copy_response.json()

    with allure.step("Validate filtered response body"):
        assert_status_code(copy_response, 201)

        assert_json_has_keys(body, ["href", "method"])
        assert body["method"] == "GET"
        assert isinstance(body["href"], str)
        assert set(body.keys()) == {"href", "method"}


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title(
    "Should return 409 when copied resource already exists and overwrite is false"
)
def test_copy_folder_without_overwrite_to_existing_path(
    client, unique_folder_name, created_folders
):
    source_folder = unique_folder_name
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        created_folders.append(source_folder)

        assert_status_code(response, 201)

    with allure.step("Create target folder"):
        response = client.create_folder(copied_folder)
        created_folders.append(copied_folder)

        assert_status_code(response, 201)

    with allure.step("Try to copy without overwrite"):
        copy_response = client.copy_resource(
            from_path=source_folder, path=copied_folder, overwrite=False
        )
        body = copy_response.json()

    with allure.step("Validate conflict response"):
        assert_status_code(copy_response, 409)

        assert_json_has_keys(body, ["error", "description", "message"])
        assert isinstance(body["error"], str)
        assert isinstance(body["description"], str)
        assert isinstance(body["message"], str)


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title("Should copy folder with overwrite true")
def test_copy_folder_with_overwrite_true(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        created_folders.append(source_folder)

        assert_status_code(response, 201)

    with allure.step("Create target folder"):
        response = client.create_folder(copied_folder)
        created_folders.append(copied_folder)

        assert_status_code(response, 201)

    with allure.step("Copy with overwrite true"):
        copy_response = client.copy_resource(
            from_path=source_folder, path=copied_folder, overwrite=True
        )
        body = copy_response.json()

    with allure.step("Validate copy response"):
        assert_status_code(copy_response, 201)
        assert_schema(body, LINK_SCHEMA)

    with allure.step("Validate target folder exists"):
        metadata_response = client.get_resource_metadata(copied_folder)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)
        assert metadata_body["type"] == "dir"
        assert metadata_body["path"] == f"disk:/{copied_folder}"


@allure.feature("Resource lifecycle")
@allure.story("Copy resource")
@allure.title("Should start async copy operation and complete successfully")
def test_copy_folder_with_force_async_true(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    copied_folder = f"{unique_folder_name}_copy"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        created_folders.append(source_folder)
        created_folders.append(copied_folder)

        assert_status_code(response, 201)

    with allure.step("Copy with force_async true"):
        copy_response = client.copy_resource(
            from_path=source_folder, path=copied_folder, force_async=True
        )
        body = copy_response.json()

    with allure.step("Validate async operation link"):
        assert_status_code(copy_response, 202)
        assert_schema(body, LINK_SCHEMA)

        assert body["method"] == "GET"
        assert body["templated"] is False
        assert "/v1/disk/operations" in body["href"]

    with allure.step("Wait until async operation is completed"):
        operation_status = None

        for _ in range(10):
            operation_response = client.get_operation_status(body["href"])
            operation_body = operation_response.json()

            assert_status_code(operation_response, 200)
            assert_schema(operation_body, OPERATION_SCHEMA)

            operation_status = operation_body["status"]

            if operation_status == "success":
                break

            assert operation_status != "failed"
            time.sleep(1)

        assert operation_status == "success"

    with allure.step("Validate copied folder exists after async operation"):
        metadata_response = client.get_resource_metadata(copied_folder)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)
        assert metadata_body["name"] == copied_folder
        assert metadata_body["type"] == "dir"
        assert metadata_body["path"] == f"disk:/{copied_folder}"
