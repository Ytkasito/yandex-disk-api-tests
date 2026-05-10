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

    def create_folder(self, path, fields=None):
        params = {"path": path}

        if fields is not None:
            params["fields"] = fields

        return requests.put(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params=params
        )

    def copy_resource(
        self,
        from_path,
        path,
        overwrite=None,
        force_async=None,
        fields=None
    ):
        params = {
            "from": from_path,
            "path": path
        }

        if overwrite is not None:
            params["overwrite"] = str(overwrite).lower()
        if force_async is not None:
            params["force_async"] = str(force_async).lower()
        if fields is not None:
            params["fields"] = fields

        return requests.post(
            f"{self.base_url}/v1/disk/resources/copy",
            headers=self.headers,
            params=params
        )

    def delete_resource(self, path, permanently=True):
        return requests.delete(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={
                "path": path,
                "permanently": str(permanently).lower()
            }
        )

    def restore_from_trash(self, path, name=None, overwrite=False):
        params = {
            "path": path,
            "overwrite": str(overwrite).lower()
        }

        if name:
            params["name"] = name

        return requests.put(
            f"{self.base_url}/v1/disk/trash/resources/restore",
            headers=self.headers,
            params=params
        )
    
    def get_resource_metadata(self, path):
        return requests.get(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={"path": path}
        )
    
    def get_trash_resource_metadata(self, path="/"):
        return requests.get(
            f"{self.base_url}/v1/disk/trash/resources",
            headers=self.headers,
            params={"path": path}
        )
    
    def move_resource(self, from_path, to_path, overwrite=False):
        return requests.post(
            f"{self.base_url}/v1/disk/resources/move",
            headers=self.headers,
            params={
                "from": from_path,
                "path": to_path,
                "overwrite": str(overwrite).lower()
            }
        )
    
    def get_resource_metadata(
        self,
        path,
        fields=None,
        limit=None,
        offset=None,
        preview_crop=None,
        preview_size=None,
        sort=None
    ):
        params = {"path": path}

        if fields is not None:
            params["fields"] = fields
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if preview_crop is not None:
            params["preview_crop"] = str(preview_crop).lower()
        if preview_size is not None:
            params["preview_size"] = preview_size
        if sort is not None:
            params["sort"] = sort

        return requests.get(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params=params
        )
    
    def get_operation_status(self, operation_href):
        return requests.get(
            operation_href,
            headers=self.headers
        )