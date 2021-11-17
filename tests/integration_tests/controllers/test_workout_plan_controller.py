import json

from tests.integration_tests.base_test import BaseTest
from tests.integration_tests.controllers.generic_controller_test import GenericControllerTest


class TestWorkoutPlanController(BaseTest, GenericControllerTest):
    def get_entity_path(self) -> str:
        return "workout-plan"

    def amount_register_items(self) -> int:
        return 2

    def get_item_to_create(self) -> dict:
        return {
            "name": "plan 1",
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
        return {
            "name": "plan 1",
            "exercises": [],
            "start_date": "2021-11-15T10:00:01.00000"
        }

    def get_default_id(self) -> str:
        return self.default_id

    def get_id_from_another_user(self) -> str:
        return "00000000-0000-0000-0000-000000000003"

    def client_api(self):
        return self.client

    @staticmethod
    def __get_exercise_plan() -> dict:
        return {
                "exercise": {
                    "id": "00000000-0000-0000-0000-000000000002"
                },
                "current_exercise_config": {
                    "sets": 5,
                    "repetitions": 10,
                    "weight": 12.5
                }
            }

    def test_create_with_invalid_exercise(self):
        item_to_create = self.get_item_to_create()
        exercise_plan = TestWorkoutPlanController.__get_exercise_plan()
        exercise_plan["exercise"]["id"] = self.get_id_from_another_user()

        item_to_create["exercises"].append(exercise_plan)

        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create,
                                          headers=self.get_authentication_header())

        self.assertEqual(403, response.status_code)

    def test_update_add_exercise(self):
        item_to_create = self.get_item_to_create()
        exercise_plan = TestWorkoutPlanController.__get_exercise_plan()
        item_to_create["exercises"].append(exercise_plan)

        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create,
                                          headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response_dto["exercises"]))

        item_to_create = response_dto
        item_to_create["exercises"] = [item_to_create["exercises"][0]]

        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create,
                                          headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_dto["exercises"]))

