RESOURCE_SCHEMA = {
    "type": "object",
    "required": [
        "name",
        "path",
        "type",
        "created",
        "modified"
    ],
    "properties": {
        "name": {
            "type": "string"
        },
        "path": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["dir", "file"]
        },
        "created": {
            "type": "string"
        },
        "modified": {
            "type": "string"
        },
        "resource_id": {
            "type": "string"
        },
        "_embedded": {
            "type": "object"
        }
    }
}