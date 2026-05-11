import os

import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from utils.assertions import (
    assert_status_code,
    assert_schema
)


pytestmark = pytest.mark.lifecycle


@allure.feature("File lifecycle")
@allure.story("Upload file")
@allure.title("Should upload file to disk")
def test_upload_file_to_disk(client):
    disk_file_path = "autotest_upload_file.txt"

    local_file_path = os.path.join(
        "test_data",
        "hello.txt"
    )

    with allure.step("Get upload link"):
        upload_link_response = client.get_upload_link(
            path=disk_file_path,
            overwrite=True
        )

        upload_link_body = upload_link_response.json()

    with allure.step("Validate upload link response"):
        assert_status_code(upload_link_response, 200)
        assert_schema(upload_link_body, LINK_SCHEMA)

        assert upload_link_body["method"] == "PUT"
        assert upload_link_body["templated"] is False

    with allure.step("Upload file using upload URL"):
        upload_response = client.upload_file(
            upload_url=upload_link_body["href"],
            file_path=local_file_path
        )

    with allure.step("Validate upload response"):
        assert upload_response.status_code in [201, 202]

    with allure.step("Validate uploaded file metadata"):
        metadata_response = client.get_resource_metadata(
            disk_file_path
        )

        metadata_body = metadata_response.json()

        assert_status_code(metadata_response, 200)

        assert metadata_body["name"] == "autotest_upload_file.txt"
        assert metadata_body["type"] == "file"

        assert metadata_body["path"] == (
            "disk:/autotest_upload_file.txt"
        )

        assert metadata_body["mime_type"] == "text/plain"

        assert metadata_body["size"] > 0

    with allure.step("Delete uploaded file"):
        delete_response = client.delete_resource(
            path=disk_file_path,
            permanently=True
        )

        assert_status_code(delete_response, 204)