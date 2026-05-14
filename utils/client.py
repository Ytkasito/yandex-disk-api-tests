import os

import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()

DEFAULT_TIMEOUT = 10


class YandexDiskClient:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.timeout = DEFAULT_TIMEOUT

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"OAuth {os.getenv('TOKEN')}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def log_response(self, response):
        logger.info(f"REQUEST: {response.request.method} {response.url}")
        logger.info(f"RESPONSE STATUS: {response.status_code}")
        logger.info(f"RESPONSE BODY: {response.text}")

    def get_disk_info(self):
        response = self.session.get(f"{self.base_url}/v1/disk", timeout=self.timeout)
        self.log_response(response)
        return response

    def create_folder(self, path, fields=None):
        params = {"path": path}
        if fields is not None:
            params["fields"] = fields

        response = self.session.put(
            f"{self.base_url}/v1/disk/resources", params=params, timeout=self.timeout
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
        sort=None,
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

        response = self.session.get(
            f"{self.base_url}/v1/disk/resources", params=params, timeout=self.timeout
        )
        self.log_response(response)
        return response

    def copy_resource(
        self, from_path, path, overwrite=None, force_async=None, fields=None
    ):
        params = {"from": from_path, "path": path}

        if overwrite is not None:
            params["overwrite"] = str(overwrite).lower()
        if force_async is not None:
            params["force_async"] = str(force_async).lower()
        if fields is not None:
            params["fields"] = fields

        response = self.session.post(
            f"{self.base_url}/v1/disk/resources/copy",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def get_operation_status(self, operation_href):
        response = self.session.get(operation_href, timeout=self.timeout)
        self.log_response(response)
        return response

    def delete_resource(
        self, path, permanently=None, md5=None, force_async=None, fields=None
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

        response = self.session.delete(
            f"{self.base_url}/v1/disk/resources", params=params, timeout=self.timeout
        )
        self.log_response(response)
        return response

    def get_trash_resource_metadata(self, path="/", limit=None, offset=None):
        params = {"path": path}

        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self.session.get(
            f"{self.base_url}/v1/disk/trash/resources",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def restore_from_trash(self, path, name=None, overwrite=None, fields=None):
        params = {"path": path}

        if name is not None:
            params["name"] = name
        if overwrite is not None:
            params["overwrite"] = str(overwrite).lower()
        if fields is not None:
            params["fields"] = fields

        response = self.session.put(
            f"{self.base_url}/v1/disk/trash/resources/restore",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def move_resource(
        self, from_path, to_path, overwrite=None, force_async=None, fields=None
    ):
        params = {"from": from_path, "path": to_path}

        if overwrite is not None:
            params["overwrite"] = str(overwrite).lower()
        if force_async is not None:
            params["force_async"] = str(force_async).lower()
        if fields is not None:
            params["fields"] = fields

        response = self.session.post(
            f"{self.base_url}/v1/disk/resources/move",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def get_upload_link(self, path, overwrite=False, fields=None):
        params = {"path": path, "overwrite": str(overwrite).lower()}
        if fields is not None:
            params["fields"] = fields

        response = self.session.get(
            f"{self.base_url}/v1/disk/resources/upload",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def upload_file(self, upload_url, file_path):
        with open(file_path, "rb") as file:
            response = requests.put(
                upload_url, files={"file": file}, timeout=self.timeout
            )
        self.log_response(response)
        return response

    def get_download_link(self, path, fields=None):
        params = {"path": path}
        if fields is not None:
            params["fields"] = fields

        response = self.session.get(
            f"{self.base_url}/v1/disk/resources/download",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def download_file(self, download_url):
        response = self.session.get(download_url, timeout=self.timeout)
        self.log_response(response)
        return response

    def publish_resource(self, path, allow_address_access=None, fields=None):
        params = {"path": path}

        if allow_address_access is not None:
            params["allow_address_access"] = str(allow_address_access).lower()
        if fields is not None:
            params["fields"] = fields

        response = self.session.put(
            f"{self.base_url}/v1/disk/resources/publish",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def unpublish_resource(self, path, fields=None):
        params = {"path": path}
        if fields is not None:
            params["fields"] = fields

        response = self.session.put(
            f"{self.base_url}/v1/disk/resources/unpublish",
            params=params,
            timeout=self.timeout,
        )
        self.log_response(response)
        return response

    def update_resource_custom_properties(self, path, custom_properties, fields=None):
        params = {"path": path}
        if fields is not None:
            params["fields"] = fields

        response = self.session.patch(
            f"{self.base_url}/v1/disk/resources",
            params=params,
            json={"custom_properties": custom_properties},
            timeout=self.timeout,
        )
        self.log_response(response)
        return response
