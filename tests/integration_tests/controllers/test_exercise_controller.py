from tests.integration_tests.controllers.test_generic_controller import TestGenericController


class TestExerciseController(TestGenericController):
    def get_entity_path(self) -> str:
        return "exercise"

    def amount_register_items(self) -> int:
        return 2

    def get_item_to_create(self) -> dict:
        return {
            "name": "Test",
            "exercise_type": "CARDIO",
            "body_type": "UPPER"
        }

    def get_invalid_item_to_create(self) -> dict:
        return {
            "name": "",
            "exercise_type": "CARDIO",
            "body_type": "UPPER"
        }

    def get_existing_id(self) -> str:
        return self.default_id
