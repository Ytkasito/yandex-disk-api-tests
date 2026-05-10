import os

import requests
from dotenv import load_dotenv


load_dotenv()


class YandexDiskClient:

    def __init__(self):

        self.base_url = os.getenv("BASE_URL")
        self.token = os.getenv("TOKEN")

        self.headers = {
            "Authorization": f"OAuth {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_disk_info(self):

        return requests.get(
            f"{self.base_url}/v1/disk",
            headers=self.headers
        )

    def create_folder(self, path):

        return requests.put(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={"path": path}
        )

    def copy_resource(self, from_path, to_path):

        return requests.post(
            f"{self.base_url}/v1/disk/resources/copy",
            headers=self.headers,
            params={
                "from": from_path,
                "path": to_path
            }
        )

    def delete_resource(self, path):

        return requests.delete(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={
                "path": path,
                "permanently": "true"
            }
        )
    
    def get_resource_metadata(self, path):
        return requests.get(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={"path": path}
        )