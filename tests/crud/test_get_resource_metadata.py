import allure
import pytest

from schemas.resource_schema import RESOURCE_SCHEMA
from utils.assertions import assert_status_code, assert_json_has_keys, assert_schema

pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Get resource metadata")
@allure.title("Should return created folder metadata with correct body")
def test_get_created_folder_metadata(client, unique_folder_name, created_folders):
    with allure.step("Create test folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Get folder metadata"):
        response = client.get_resource_metadata(unique_folder_name)
        body = response.json()

    with allure.step("Validate status code"):
        assert_status_code(response, 200)

    with allure.step("Validate response schema"):
        assert_schema(body, RESOURCE_SCHEMA)

    with allure.step("Validate main folder fields"):
        assert body["name"] == unique_folder_name
        assert body["type"] == "dir"
        assert body["path"] == f"disk:/{unique_folder_name}"

    with allure.step("Validate required fields exist"):
        assert_json_has_keys(body, ["created", "modified", "resource_id", "_embedded"])

    with allure.step("Validate field types"):
        assert isinstance(body["name"], str)
        assert isinstance(body["type"], str)
        assert isinstance(body["path"], str)
        assert isinstance(body["created"], str)
        assert isinstance(body["modified"], str)
        assert isinstance(body["resource_id"], str)
        assert isinstance(body["_embedded"], dict)

    with allure.step("Validate embedded resource list"):
        embedded = body["_embedded"]

        assert embedded["path"] == f"disk:/{unique_folder_name}"
        assert isinstance(embedded["items"], list)
        assert isinstance(embedded["limit"], int)
        assert isinstance(embedded["offset"], int)


@allure.feature("Resource CRUD")
@allure.story("Get resource metadata")
@allure.title("Should return only requested fields")
def test_get_resource_metadata_with_fields(client, unique_folder_name, created_folders):
    with allure.step("Create test folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Get metadata with fields filter"):
        response = client.get_resource_metadata(
            path=unique_folder_name, fields="name,type,path"
        )
        body = response.json()

    with allure.step("Validate status code"):
        assert_status_code(response, 200)

    with allure.step("Validate filtered response body"):
        assert_json_has_keys(body, ["name", "type", "path"])

        assert body["name"] == unique_folder_name
        assert body["type"] == "dir"
        assert body["path"] == f"disk:/{unique_folder_name}"

        assert set(body.keys()) == {"name", "type", "path"}


@allure.feature("Resource CRUD")
@allure.story("Get resource metadata")
@allure.title("Should return embedded list with limit and offset")
def test_get_folder_metadata_with_limit_and_offset(
    client, unique_folder_name, created_folders
):
    child_folder_1 = f"{unique_folder_name}/child_1"
    child_folder_2 = f"{unique_folder_name}/child_2"

    with allure.step("Create parent folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Create child folders"):
        assert_status_code(client.create_folder(child_folder_1), 201)
        assert_status_code(client.create_folder(child_folder_2), 201)

    with allure.step("Get metadata with limit and offset"):
        response = client.get_resource_metadata(
            path=unique_folder_name, limit=1, offset=1
        )
        body = response.json()

    with allure.step("Validate status code"):
        assert_status_code(response, 200)

    with allure.step("Validate pagination fields"):
        embedded = body["_embedded"]

        assert embedded["limit"] == 1
        assert embedded["offset"] == 1
        assert len(embedded["items"]) == 1
