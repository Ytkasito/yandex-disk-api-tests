import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from utils.assertions import assert_status_code, assert_schema, assert_json_has_keys

pytestmark = pytest.mark.lifecycle


@allure.feature("Public access lifecycle")
@allure.story("Publish and unpublish resource")
@allure.title("Should publish and unpublish folder")
def test_publish_and_unpublish_folder(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Publish folder"):
        publish_response = client.publish_resource(unique_folder_name)
        publish_body = publish_response.json()

    with allure.step("Validate publish response"):
        assert_status_code(publish_response, 200)
        assert_schema(publish_body, LINK_SCHEMA)

        assert publish_body["method"] == "GET"
        assert publish_body["templated"] is False

    with allure.step("Get published folder metadata"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        metadata_body = metadata_response.json()

    with allure.step("Validate public fields in metadata"):
        assert_status_code(metadata_response, 200)
        assert_json_has_keys(metadata_body, ["public_key", "public_url"])

        assert isinstance(metadata_body["public_key"], str)
        assert isinstance(metadata_body["public_url"], str)

        assert len(metadata_body["public_key"]) > 0
        assert metadata_body["public_url"].startswith("https://")

    with allure.step("Unpublish folder"):
        unpublish_response = client.unpublish_resource(unique_folder_name)
        unpublish_body = unpublish_response.json()

    with allure.step("Validate unpublish response"):
        assert_status_code(unpublish_response, 200)
        assert_schema(unpublish_body, LINK_SCHEMA)

        assert unpublish_body["method"] == "GET"
        assert unpublish_body["templated"] is False

    with allure.step("Get folder metadata after unpublish"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        metadata_body = metadata_response.json()

    with allure.step("Validate public fields are removed"):
        assert_status_code(metadata_response, 200)

        assert "public_key" not in metadata_body
        assert "public_url" not in metadata_body
