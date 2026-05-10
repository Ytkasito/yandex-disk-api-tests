import uuid

import pytest

from utils.client import YandexDiskClient


@pytest.fixture
def client():
    return YandexDiskClient()


@pytest.fixture
def unique_folder_name():
    return f"test_folder_{uuid.uuid4().hex}"