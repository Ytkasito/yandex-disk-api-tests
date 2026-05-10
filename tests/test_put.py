from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_create_folder(client, unique_folder_name):
    response = client.create_folder(unique_folder_name)

    assert response.status_code == 201