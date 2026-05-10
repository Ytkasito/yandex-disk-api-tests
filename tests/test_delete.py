from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_delete_folder():

    client.create_folder("folder_to_delete")

    response = client.delete_resource(
        "folder_to_delete"
    )

    assert response.status_code in [202, 204]