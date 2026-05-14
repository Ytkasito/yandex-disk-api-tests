import os

import allure
import pytest

from schemas.link_schema import LINK_SCHEMA
from utils.assertions import assert_status_code, assert_schema

pytestmark = pytest.mark.lifecycle


@allure.feature("File lifecycle")
@allure.story("Download file")
@allure.title("Should download uploaded file from disk")
def test_download_uploaded_file_from_disk(client):
    disk_file_path = "autotest_download_file.txt"
    local_file_path = os.path.join("test_data", "hello.txt")

    with allure.step("Read local file content"):
        with open(local_file_path, "rb") as file:
            expected_content = file.read()

    with allure.step("Get upload link"):
        upload_link_response = client.get_upload_link(
            path=disk_file_path, overwrite=True
        )
        upload_link_body = upload_link_response.json()

        assert_status_code(upload_link_response, 200)
        assert_schema(upload_link_body, LINK_SCHEMA)

    with allure.step("Upload file"):
        upload_response = client.upload_file(
            upload_url=upload_link_body["href"], file_path=local_file_path
        )

        assert upload_response.status_code in [201, 202]

    with allure.step("Get download link"):
        download_link_response = client.get_download_link(path=disk_file_path)
        download_link_body = download_link_response.json()

        assert_status_code(download_link_response, 200)
        assert_schema(download_link_body, LINK_SCHEMA)

        assert download_link_body["method"] == "GET"
        assert download_link_body["templated"] is False

    with allure.step("Download file by link"):
        download_response = client.download_file(
            download_url=download_link_body["href"]
        )

        assert_status_code(download_response, 200)

    with allure.step("Validate downloaded file content"):
        assert download_response.content == expected_content

    with allure.step("Delete uploaded file"):
        delete_response = client.delete_resource(path=disk_file_path, permanently=True)

        assert_status_code(delete_response, 204)
