from typing import List


class InvalidEntityException(Exception):
    def __init__(self, entity_name: str, missing_fields: List[str]):
        super().__init__(f"Invalid {entity_name} missing the following fields: {missing_fields}")
