ERROR_SCHEMA = {
    "type": "object",
    "required": ["error", "description", "message"],
    "properties": {
        "error": {"type": "string"},
        "description": {"type": "string"},
        "message": {"type": "string"},
        "details": {"type": "object"},
    },
}
