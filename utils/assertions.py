import json

import allure
from jsonschema import validate

from schemas.error_schema import ERROR_SCHEMA


def attach_response(response):
    allure.attach(
        str(response.status_code),
        name="Response status",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        response.request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        response.request.method,
        name="Request method",
        attachment_type=allure.attachment_type.TEXT,
    )

    if response.text:
        try:
            body = json.dumps(response.json(), indent=4, ensure_ascii=False)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
    else:
        body = "Empty response body"
        attachment_type = allure.attachment_type.TEXT

    allure.attach(body, name="Response body", attachment_type=attachment_type)


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
        attachment_type=allure.attachment_type.JSON,
    )

    validate(instance=body, schema=schema)


def assert_error_response(body):
    assert_schema(body, ERROR_SCHEMA)


def assert_response_time(response, max_seconds=5.0):
    """Assert that the response was received within the time limit."""
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, (
        f"Response took {elapsed:.2f}s, expected <= {max_seconds}s. "
        f"URL: {response.url}"
    )


def assert_field_value(body, field, expected_value):
    """Assert that a specific field in the response body has the expected value."""
    assert field in body, f"Field '{field}' not found in response body"
    actual = body[field]
    assert (
        actual == expected_value
    ), f"Field '{field}': expected {expected_value!r}, got {actual!r}"


def assert_field_type(body, field, expected_type):
    """Assert that a specific field in the response body is of the expected type."""
    assert field in body, f"Field '{field}' not found in response body"
    actual = body[field]
    assert isinstance(actual, expected_type), (
        f"Field '{field}': expected type {expected_type.__name__}, "
        f"got {type(actual).__name__}"
    )


def assert_json_keys_only(body, expected_keys):
    """Assert that the response body contains exactly the expected keys, no more, no less."""
    actual_keys = set(body.keys())
    expected = set(expected_keys)
    assert actual_keys == expected, (
        f"Response body keys mismatch.\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual_keys)}\n"
        f"Extra: {sorted(actual_keys - expected)}\n"
        f"Missing: {sorted(expected - actual_keys)}"
    )
