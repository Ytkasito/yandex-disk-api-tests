from jsonschema import validate


def assert_status_code(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, "
        f"but got {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_json_has_keys(body, keys):
    for key in keys:
        assert key in body, f"Key '{key}' not found in response"


def assert_schema(body, schema):
    validate(instance=body, schema=schema)