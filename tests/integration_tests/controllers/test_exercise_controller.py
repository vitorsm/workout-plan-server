from tests.integration_tests.base_test import BaseTest
from tests.integration_tests.controllers.generic_controller_test import GenericControllerTest


class TestExerciseController(BaseTest, GenericControllerTest):

    def get_id_from_another_user(self) -> str:
        return "00000000-0000-0000-0000-000000000003"

    def get_default_id(self) -> str:
        return self.default_id

    def client_api(self):
        return self.client

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
