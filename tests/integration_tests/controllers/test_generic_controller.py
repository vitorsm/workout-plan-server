import abc
import json

from tests.integration_tests.base_test import BaseTest


class TestGenericController(BaseTest, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_entity_path(self) -> str:
        raise NotImplementedError

    def amount_register_items(self) -> int:
        raise NotImplementedError

    def get_item_to_create(self) -> dict:
        raise NotImplementedError

    def get_invalid_item_to_create(self) -> dict:
        raise NotImplementedError

    def get_existing_id(self) -> str:
        raise NotImplementedError

    def get_base_endpoint(self) -> str:
        return f"/v1/{self.get_entity_path()}/"

    def test_find_by_id(self):
        response = self.client.get(f"{self.get_base_endpoint()}{self.default_id}")
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.__assert_each_item(response_dto)
        self.assertEqual(self.default_id, response_dto["id"])

    def test_find_all(self):
        response = self.client.get(self.get_base_endpoint())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.amount_register_items(), len(response_dto))
        [self.__assert_each_item(item) for item in response_dto]

    def test_create(self):
        item_to_create = self.get_item_to_create()
        response = self.client.post(self.get_base_endpoint(), json=item_to_create)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)

        self.__assert_equal_item(item_to_create, response_dto)

    def test_invalid_creation(self):
        item_to_create = self.get_invalid_item_to_create()
        response = self.client.post(self.get_base_endpoint(), json=item_to_create)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_update(self):
        item_to_update = self.get_item_to_create()
        item_to_update["id"] = self.get_existing_id()

        response = self.client.put(f"{self.get_base_endpoint()}{self.default_id}", json=item_to_update)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.__assert_equal_item(item_to_update, response_dto)

    def test_invalid_update(self):
        item_to_update = self.get_invalid_item_to_create()
        item_to_update["id"] = self.get_existing_id()

        response = self.client.put(f"{self.get_base_endpoint()}{self.default_id}", json=item_to_update)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_delete(self):
        response = self.client.get(f"{self.get_base_endpoint()}{self.default_id}")
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto)

        response = self.client.delete(f"{self.get_base_endpoint()}{self.default_id}")
        self.assertEqual(204, response.status_code)

        response = self.client.get(f"{self.get_base_endpoint()}{self.default_id}")
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNone(response_dto)

    def __assert_equal_item(self, item_a: dict, item_b: dict):
        for key, value in item_a.items():
            self.assertEqual(value, item_b[key])

    def __assert_each_item(self, item_dto: dict):
        self.assertIsNotNone(item_dto["name"])
        self.assertIsNotNone(item_dto["created_by"])
        self.assertIsNotNone(item_dto["created_at"])
        self.assertIsNotNone(item_dto["modified_at"])
