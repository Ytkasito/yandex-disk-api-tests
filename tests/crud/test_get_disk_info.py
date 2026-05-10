import allure
import pytest


pytestmark = pytest.mark.crud


@allure.feature("Disk information")
@allure.story("Get disk info")
@allure.title("Should return disk information")
def test_get_disk_info(client):
    with allure.step("Get disk information"):
        response = client.get_disk_info()

    with allure.step("Check response status and required fields"):
        body = response.json()

        assert response.status_code == 200
        assert "trash_size" in body
        assert "total_space" in body
        assert "used_space" in body
        assert "system_folders" in body
