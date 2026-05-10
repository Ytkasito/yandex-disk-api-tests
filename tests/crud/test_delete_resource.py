from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_delete_folder(client, unique_folder_name):
    client.create_folder(unique_folder_name)

    response = client.delete_resource(unique_folder_name)

    assert response.status_code in [202, 204]