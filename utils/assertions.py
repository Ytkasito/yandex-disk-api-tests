import allure
import json
from jsonschema import validate
from schemas.error_schema import ERROR_SCHEMA

def attach_response(response):
    allure.attach(
        response.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        str(response.status_code),
        name="Status Code",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        response.text,
        name="Response Body",
        attachment_type=allure.attachment_type.JSON
    )


def assert_status_code(response, expected_status):
    attach_response(response)

    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, "
        f"but got {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_json_has_keys(body, keys):
    for key in keys:
        assert key in body, f"Key '{key}' not found in response"


def assert_schema(body, schema):
    allure.attach(
        str(body),
        name="JSON Body For Schema Validation",
        attachment_type=allure.attachment_type.JSON
    )

    validate(instance=body, schema=schema)

def assert_error_response(body):
    assert_schema(body, ERROR_SCHEMA)

def attach_response(response):
    allure.attach(
        str(response.status_code),
        name="Response status",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        response.request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        response.request.method,
        name="Request method",
        attachment_type=allure.attachment_type.TEXT
    )

    if response.text:
        try:
            body = json.dumps(
                response.json(),
                indent=4,
                ensure_ascii=False
            )
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
    else:
        body = "Empty response body"
        attachment_type = allure.attachment_type.TEXT

    allure.attach(
        body,
        name="Response body",
        attachment_type=attachment_type
    )