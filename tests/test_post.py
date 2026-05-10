from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_copy_folder():

    client.create_folder("source_folder")

    response = client.copy_resource(
        "source_folder",
        "copied_folder"
    )

    assert response.status_code in [201, 202]