LINK_SCHEMA = {
    "type": "object",
    "required": ["href", "method", "templated"],
    "properties": {
        "href": {"type": "string"},
        "method": {"type": "string"},
        "templated": {"type": "boolean"}
    }
}