import pytest
import requests


pytestmark = pytest.mark.negative


def test_should_return_409_when_creating_existing_folder(
        client,
        unique_folder_name,
        created_folders
):
    first_response = client.create_folder(unique_folder_name)
    created_folders.append(unique_folder_name)

    second_response = client.create_folder(unique_folder_name)

    assert first_response.status_code == 201
    assert second_response.status_code == 409

    body = second_response.json()

    assert body["error"] == "DiskPathPointsToExistentDirectoryError"


def test_should_return_404_for_non_existing_resource(client):
    response = client.get_resource_metadata(
        "definitely_non_existing_folder"
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"] == "DiskNotFoundError"


def test_should_return_401_without_oauth_token():
    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk"
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"] == "UnauthorizedError"