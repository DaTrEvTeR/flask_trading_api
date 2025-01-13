def is_data_full(data: dict, *required_fields: str) -> bool:
    if data:
        return all([(field in data) for field in required_fields])
    return False
