

class EntityNotFoundException(Exception):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(f"{entity} {entity_id} was not found")
