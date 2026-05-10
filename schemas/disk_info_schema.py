DISK_INFO_SCHEMA = {
    "type": "object",
    "required": [
        "trash_size",
        "total_space",
        "used_space",
        "system_folders"
    ],
    "properties": {
        "trash_size": {"type": "integer"},
        "total_space": {"type": "integer"},
        "used_space": {"type": "integer"},
        "system_folders": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        }
    }
}