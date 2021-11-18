from tests.integration_tests.base_test import BaseTest
from tests.integration_tests.controllers.generic_controller_test import GenericControllerTest


class TestTrainingController(BaseTest, GenericControllerTest):
    def get_entity_path(self) -> str:
        return "training"

    def amount_register_items(self) -> int:
        return 2

    def get_item_to_create(self) -> dict:
        return {
            "exercises": [{
                "exercise": {
                    "id": "00000000-0000-0000-0000-000000000001"
                },
                "current_exercise_config": {
                    "sets": 3,
                    "repetitions": 12,
                    "weight": 12.5
                }
            }],
            "start_date": "2021-11-15T10:00:01"
        }

    def get_invalid_item_to_create(self) -> dict:
        return {}

    def get_default_id(self) -> str:
        return self.default_id

    def get_id_from_another_user(self) -> str:
        return "00000000-0000-0000-0000-000000000003"

    def client_api(self):
        return self.client
