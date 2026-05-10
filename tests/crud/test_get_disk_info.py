import allure
import pytest

from utils.assertions import (
    assert_status_code,
    assert_json_has_keys,
    assert_schema
)

from schemas.disk_info_schema import DISK_INFO_SCHEMA

pytestmark = pytest.mark.crud


@allure.feature("Disk information")
@allure.story("Get disk info")
@allure.title("Should return complete disk information")
def test_get_disk_info(client):
    with allure.step("Get disk information"):
        response = client.get_disk_info()
        body = response.json()

    with allure.step("Validate status code"):
        assert_status_code(response, 200)

    with allure.step("Validate response schema"):
        assert_schema(body, DISK_INFO_SCHEMA)

    with allure.step("Validate required root fields"):
        assert_json_has_keys(body, [
            "trash_size",
            "total_space",
            "used_space",
            "system_folders"
        ])

    with allure.step("Validate field types"):
        assert isinstance(body["trash_size"], int)
        assert isinstance(body["total_space"], int)
        assert isinstance(body["used_space"], int)
        assert isinstance(body["system_folders"], dict)

    with allure.step("Validate disk space values"):
        assert body["total_space"] > 0
        assert body["used_space"] >= 0
        assert body["trash_size"] >= 0

    with allure.step("Validate used space does not exceed total space"):
        assert body["used_space"] <= body["total_space"]

    with allure.step("Validate system folders structure"):
        system_folders = body["system_folders"]

        assert isinstance(system_folders, dict)
        assert len(system_folders) > 0

    with allure.step("Validate all system folder values are strings"):
        for folder_name, folder_path in system_folders.items():
            assert isinstance(folder_name, str)
            assert isinstance(folder_path, str)

            assert folder_path.startswith("disk:/")
