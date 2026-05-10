import os

import requests
from dotenv import load_dotenv

from utils.logger import logger


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

    def log_response(self, response):
        logger.info(f"REQUEST: {response.request.method} {response.url}")
        logger.info(f"RESPONSE STATUS: {response.status_code}")
        logger.info(f"RESPONSE BODY: {response.text}")

    def get_disk_info(self):
        response = requests.get(
            f"{self.base_url}/v1/disk",
            headers=self.headers
        )

        self.log_response(response)

        return response

    def create_folder(self, path, fields=None):
        params = {"path": path}

        if fields is not None:
            params["fields"] = fields

        response = requests.put(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params=params
        )

        self.log_response(response)

        return response

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

        response = requests.get(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params=params
        )

        self.log_response(response)

        return response

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

        response = requests.post(
            f"{self.base_url}/v1/disk/resources/copy",
            headers=self.headers,
            params=params
        )

        self.log_response(response)

        return response

    def get_operation_status(self, operation_href):
        response = requests.get(
            operation_href,
            headers=self.headers
        )

        self.log_response(response)

        return response

    def delete_resource(
        self,
        path,
        permanently=None,
        md5=None,
        force_async=None,
        fields=None
    ):
        params = {"path": path}

        if permanently is not None:
            params["permanently"] = str(permanently).lower()
        if md5 is not None:
            params["md5"] = md5
        if force_async is not None:
            params["force_async"] = str(force_async).lower()
        if fields is not None:
            params["fields"] = fields

        response = requests.delete(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params=params
        )

        self.log_response(response)

        return response

    def get_trash_resource_metadata(self, path="/"):
        response = requests.get(
            f"{self.base_url}/v1/disk/trash/resources",
            headers=self.headers,
            params={"path": path}
        )

        self.log_response(response)

        return response

    def restore_from_trash(self, path, name=None, overwrite=False):
        params = {
            "path": path,
            "overwrite": str(overwrite).lower()
        }

        if name:
            params["name"] = name

        response = requests.put(
            f"{self.base_url}/v1/disk/trash/resources/restore",
            headers=self.headers,
            params=params
        )

        self.log_response(response)

        return response

    def move_resource(self, from_path, to_path, overwrite=False):
        response = requests.post(
            f"{self.base_url}/v1/disk/resources/move",
            headers=self.headers,
            params={
                "from": from_path,
                "path": to_path,
                "overwrite": str(overwrite).lower()
            }
        )

        self.log_response(response)

        return response