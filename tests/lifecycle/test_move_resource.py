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
@allure.story("Move resource")
@allure.title("Should move empty folder and return link body")
def test_move_empty_folder(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    moved_folder = f"{unique_folder_name}_moved"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)
        assert_status_code(create_response, 201)

    with allure.step("Move source folder"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=moved_folder
        )
        body = move_response.json()
        created_folders.append(moved_folder)

    with allure.step("Validate move response"):
        assert_status_code(move_response, 201)
        assert_schema(body, LINK_SCHEMA)
        assert_json_has_keys(body, ["href", "method", "templated"])

        assert body["method"] == "GET"
        assert body["templated"] is False
        assert isinstance(body["href"], str)

    with allure.step("Validate old folder path does not exist"):
        old_metadata_response = client.get_resource_metadata(source_folder)
        old_body = old_metadata_response.json()

        assert_status_code(old_metadata_response, 404)
        assert_json_has_keys(old_body, ["error", "description", "message"])

    with allure.step("Validate moved folder metadata"):
        metadata_response = client.get_resource_metadata(moved_folder)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)
        assert metadata_body["name"] == moved_folder
        assert metadata_body["type"] == "dir"
        assert metadata_body["path"] == f"disk:/{moved_folder}"


@allure.feature("Resource lifecycle")
@allure.story("Move resource")
@allure.title("Should move folder with fields filter")
def test_move_folder_with_fields_filter(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    moved_folder = f"{unique_folder_name}_moved"

    with allure.step("Create source folder"):
        create_response = client.create_folder(source_folder)
        assert_status_code(create_response, 201)

    with allure.step("Move source folder with fields filter"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=moved_folder,
            fields="href,method"
        )
        body = move_response.json()
        created_folders.append(moved_folder)

    with allure.step("Validate filtered response body"):
        assert_status_code(move_response, 201)

        assert_json_has_keys(body, ["href", "method"])
        assert body["method"] == "GET"
        assert isinstance(body["href"], str)
        assert set(body.keys()) == {"href", "method"}


@allure.feature("Resource lifecycle")
@allure.story("Move resource")
@allure.title("Should return 409 when target already exists and overwrite is false")
def test_move_folder_without_overwrite_to_existing_path(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    target_folder = f"{unique_folder_name}_target"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        created_folders.append(source_folder)
        assert_status_code(response, 201)

    with allure.step("Create target folder"):
        response = client.create_folder(target_folder)
        created_folders.append(target_folder)
        assert_status_code(response, 201)

    with allure.step("Try to move without overwrite"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=target_folder,
            overwrite=False
        )
        body = move_response.json()

    with allure.step("Validate conflict response"):
        assert_status_code(move_response, 409)
        assert_json_has_keys(body, ["error", "description", "message"])

        assert isinstance(body["error"], str)
        assert isinstance(body["description"], str)
        assert isinstance(body["message"], str)


@allure.feature("Resource lifecycle")
@allure.story("Move resource")
@allure.title("Should move folder with overwrite true")
def test_move_folder_with_overwrite_true(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    target_folder = f"{unique_folder_name}_target"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        created_folders.append(target_folder)
        assert_status_code(response, 201)

    with allure.step("Create target folder"):
        response = client.create_folder(target_folder)
        assert_status_code(response, 201)

    with allure.step("Move with overwrite true"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=target_folder,
            overwrite=True
        )
        body = move_response.json()

    with allure.step("Validate move response"):
        assert_status_code(move_response, 201)
        assert_schema(body, LINK_SCHEMA)

    with allure.step("Validate source folder no longer exists"):
        source_metadata_response = client.get_resource_metadata(source_folder)
        assert_status_code(source_metadata_response, 404)

    with allure.step("Validate target folder exists"):
        metadata_response = client.get_resource_metadata(target_folder)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)
        assert metadata_body["type"] == "dir"
        assert metadata_body["path"] == f"disk:/{target_folder}"


@allure.feature("Resource lifecycle")
@allure.story("Move resource")
@allure.title("Should start async move operation when force_async is true")
def test_move_folder_with_force_async_true(client, unique_folder_name, created_folders):
    source_folder = unique_folder_name
    moved_folder = f"{unique_folder_name}_moved"

    with allure.step("Create source folder"):
        response = client.create_folder(source_folder)
        assert_status_code(response, 201)

    with allure.step("Move with force_async true"):
        move_response = client.move_resource(
            from_path=source_folder,
            to_path=moved_folder,
            force_async=True
        )
        body = move_response.json()
        created_folders.append(moved_folder)

    with allure.step("Validate async operation link"):
        assert_status_code(move_response, 202)
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