from utils.client import YandexDiskClient


def test_get_disk_info():
    client = YandexDiskClient()

    response = client.get_disk_info()

    assert response.status_code == 200
