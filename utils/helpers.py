import time

from utils.logger import logger


def wait_for_operation(client, operation_href, timeout=30, poll_interval=1.0):
    """
    Poll an async operation until it completes or the timeout is exceeded.

    Returns the final operation status response.
    Raises TimeoutError if the operation does not complete within the timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        response = client.get_operation_status(operation_href)
        if response.status_code != 200:
            return response

        body = response.json()
        status = body.get("status")

        logger.info(f"Operation status: {status}")

        if status == "success":
            return response
        if status == "failed":
            return response

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Operation at {operation_href} did not complete within {timeout}s"
    )
