

class DuplicateEntityException(Exception):
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(f"The {entity} is duplicate - {field}: {value}")
