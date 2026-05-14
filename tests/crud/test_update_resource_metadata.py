import allure
import pytest

from schemas.resource_schema import RESOURCE_SCHEMA
from utils.assertions import assert_status_code, assert_schema

pytestmark = pytest.mark.crud


@allure.feature("Resource CRUD")
@allure.story("Update resource metadata")
@allure.title("Should add custom properties to folder")
def test_add_custom_properties_to_folder(client, unique_folder_name, created_folders):
    custom_properties = {"project": "yandex-disk-api-tests", "created_by": "pytest"}

    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Add custom properties"):
        patch_response = client.update_resource_custom_properties(
            path=unique_folder_name, custom_properties=custom_properties
        )
        patch_body = patch_response.json()

    with allure.step("Validate patch response"):
        assert_status_code(patch_response, 200)
        assert_schema(patch_body, RESOURCE_SCHEMA)

        assert patch_body["custom_properties"]["project"] == "yandex-disk-api-tests"
        assert patch_body["custom_properties"]["created_by"] == "pytest"

    with allure.step("Validate custom properties in metadata"):
        metadata_response = client.get_resource_metadata(unique_folder_name)
        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)

        assert metadata_body["custom_properties"]["project"] == "yandex-disk-api-tests"
        assert metadata_body["custom_properties"]["created_by"] == "pytest"


@allure.feature("Resource CRUD")
@allure.story("Update resource metadata")
@allure.title("Should update existing custom property")
def test_update_existing_custom_property(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Add initial custom property"):
        response = client.update_resource_custom_properties(
            path=unique_folder_name, custom_properties={"status": "draft"}
        )

        assert_status_code(response, 200)

    with allure.step("Update custom property"):
        response = client.update_resource_custom_properties(
            path=unique_folder_name, custom_properties={"status": "ready"}
        )
        body = response.json()

    with allure.step("Validate updated custom property"):
        assert_status_code(response, 200)

        assert body["custom_properties"]["status"] == "ready"


@allure.feature("Resource CRUD")
@allure.story("Update resource metadata")
@allure.title("Should remove custom property when value is null")
def test_remove_custom_property(client, unique_folder_name, created_folders):
    with allure.step("Create folder"):
        create_response = client.create_folder(unique_folder_name)
        created_folders.append(unique_folder_name)

        assert_status_code(create_response, 201)

    with allure.step("Add custom property"):
        response = client.update_resource_custom_properties(
            path=unique_folder_name, custom_properties={"temporary": "true"}
        )

        assert_status_code(response, 200)

    with allure.step("Remove custom property"):
        response = client.update_resource_custom_properties(
            path=unique_folder_name, custom_properties={"temporary": None}
        )
        body = response.json()

    with allure.step("Validate custom property removed"):
        assert_status_code(response, 200)

        custom_properties = body.get("custom_properties")

        assert custom_properties is None or "temporary" not in custom_properties
