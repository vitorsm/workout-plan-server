import json

from tests.integration_tests.base_test import BaseTest
from tests.integration_tests.controllers.generic_controller_test import GenericControllerTest


class TestTrainingController(BaseTest, GenericControllerTest):
    def get_entity_path(self) -> str:
        return "training"

    def amount_register_items(self) -> int:
        return 2

    def get_item_to_create(self) -> dict:
        return {
            "workout_plan": {
                "id": "00000000-0000-0000-0000-000000000001"
            },
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

    def test_find_by_id_checking_fields(self):
        response = self._find_by_id()
        response_dto = json.loads(response.data.decode())

        self.assertIsNotNone(response_dto["workout_plan"])
        self.assertIsNotNone(response_dto["workout_plan"]["name"])
        self.assertEqual(2, len(response_dto["workout_plan"]["exercises"]))

    def test_update_adding_exercises(self):
        entity_id = "00000000-0000-0000-0000-000000000002"
        response = self._find_by_id(entity_id)
        item_to_update = json.loads(response.data.decode())

        item_to_update["exercises"].append({
                "exercise": {
                    "id": "00000000-0000-0000-0000-000000000002"
                },
                "current_exercise_config": {
                    "sets": 3,
                    "repetitions": 12,
                    "weight": 12.5
                }
            })

        response = self.client_api().put(self._get_endpoint_by_id(entity_id), json=item_to_update,
                                         headers=self.get_authentication_header())

        self.assertEqual(200, response.status_code)

        response = self._find_by_id(entity_id)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(1, len(response_dto["exercises"]))

        item_to_update = response_dto

        item_to_update["exercises"].append({
            "exercise": {
                "id": "00000000-0000-0000-0000-000000000001"
            },
            "current_exercise_config": {
                "sets": 2,
                "repetitions": 12,
                "weight": 12.5
            }
        })

        response = self.client_api().put(self._get_endpoint_by_id(entity_id), json=item_to_update,
                                         headers=self.get_authentication_header())

        self.assertEqual(200, response.status_code)

        response = self._find_by_id(entity_id)
        response_dto = json.loads(response.data.decode())
        self.assertEqual(2, len(response_dto["exercises"]))
