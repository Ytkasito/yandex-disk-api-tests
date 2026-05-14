import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from utils.assertions import assert_status_code, assert_json_has_keys, assert_schema

pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Create folder")
@allure.title("Should create folder and return link body")
def test_create_folder_returns_link_body(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        response = client.create_folder(unique_folder_name)
        body = response.json()

        created_folders.append(unique_folder_name)

    with allure.step("Validate status code"):
        assert_status_code(response, 201)

    with allure.step("Validate response schema"):
        assert_schema(body, LINK_SCHEMA)

    with allure.step("Validate required link fields"):
        assert_json_has_keys(body, ["href", "method", "templated"])

    with allure.step("Validate link body values"):
        assert body["method"] == "GET"
        assert body["templated"] is False
        assert isinstance(body["href"], str)
        assert "/v1/disk/resources" in body["href"]
        assert "path=" in body["href"]


@allure.feature("Resource CRUD")
@allure.story("Create folder")
@allure.title("Should create folder with fields filter")
def test_create_folder_with_fields_filter(client, unique_folder_name, created_folders):
    with allure.step("Create folder with fields filter"):
        response = client.create_folder(path=unique_folder_name, fields="href,method")
        body = response.json()

        created_folders.append(unique_folder_name)

    with allure.step("Validate status code"):
        assert_status_code(response, 201)

    with allure.step("Validate filtered response body"):
        assert_json_has_keys(body, ["href", "method"])

        assert body["method"] == "GET"
        assert isinstance(body["href"], str)
        assert set(body.keys()) == {"href", "method"}


@allure.feature("Resource CRUD")
@allure.story("Create folder")
@allure.title("Should create nested folder when parent exists")
def test_create_nested_folder_when_parent_exists(
    client, unique_folder_name, created_folders
):
    parent_folder = unique_folder_name
    child_folder = f"{unique_folder_name}/child"

    with allure.step("Create parent folder"):
        parent_response = client.create_folder(parent_folder)
        created_folders.append(parent_folder)

        assert_status_code(parent_response, 201)

    with allure.step("Create child folder"):
        child_response = client.create_folder(child_folder)

        assert_status_code(child_response, 201)

    with allure.step("Get child folder metadata"):
        metadata_response = client.get_resource_metadata(child_folder)
        body = metadata_response.json()

    with allure.step("Validate child folder metadata"):
        assert_status_code(metadata_response, 200)

        assert body["name"] == "child"
        assert body["type"] == "dir"
        assert body["path"] == f"disk:/{child_folder}"
