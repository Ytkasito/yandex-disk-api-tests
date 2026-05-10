from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_copy_folder(client):
    source_folder = "source_folder"
    copied_folder = "copied_folder"

    client.delete_resource(source_folder)
    client.delete_resource(copied_folder)

    client.create_folder(source_folder)

    response = client.copy_resource(
        source_folder,
        copied_folder
    )

    assert response.status_code in [201, 202]