OPERATION_SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {"type": "string", "enum": ["success", "failed", "in-progress"]}
    },
}
