def is_data_have_one_of_the_attributes(data: dict, *required_fields: str) -> bool:
    if data:
        return any([(field in data) for field in required_fields])
    return False
