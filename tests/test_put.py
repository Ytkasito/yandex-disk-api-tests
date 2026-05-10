from utils.client import YandexDiskClient


client = YandexDiskClient()


def test_create_folder():

    response = client.create_folder("test_folder")

    assert response.status_code == 201