import abc
import json
from typing import Optional


class GenericControllerTest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_entity_path(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def amount_register_items(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_item_to_create(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_invalid_item_to_create(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_id(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_id_from_another_user(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authentication_header(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def client_api(self):
        raise NotImplementedError

    @abc.abstractmethod
    def assertEqual(self, expected, actual):
        raise NotImplementedError

    @abc.abstractmethod
    def assertIsNotNone(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def assertIsNone(self, item):
        raise NotImplementedError

    def get_base_endpoint(self) -> str:
        return f"/v1/{self.get_entity_path()}/"

    def _get_endpoint_by_id(self, entity_id: Optional[str] = None) -> str:
        if not entity_id:
            entity_id = self.get_default_id()

        return f"{self.get_base_endpoint()}{entity_id}"

    def _find_by_id(self, entity_id: Optional[str] = None):
        return self.client_api().get(self._get_endpoint_by_id(entity_id), headers=self.get_authentication_header())

    def test_find_by_id(self):
        response = self._find_by_id()
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.__assert_each_item(response_dto)
        self.assertEqual(self.get_default_id(), response_dto["id"])

    def test_find_by_id_without_login(self):
        response = self.client_api().get(self._get_endpoint_by_id())
        self.assertEqual(401, response.status_code)

    def test_find_by_id_from_another_user(self):
        response = self.client_api().get(self._get_endpoint_by_id(self.get_id_from_another_user()),
                                         headers=self.get_authentication_header())
        self.assertEqual(403, response.status_code)

    def test_find_all(self):
        response = self.client_api().get(self.get_base_endpoint(), headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.amount_register_items(), len(response_dto))
        [self.__assert_each_item(item) for item in response_dto]

    def test_find_all_without_login(self):
        response = self.client_api().get(self.get_base_endpoint())
        self.assertEqual(401, response.status_code)

    def test_create(self):
        item_to_create = self.get_item_to_create()
        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create,
                                          headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)

        self.__assert_equal_item(item_to_create, response_dto)

    def test_create_without_login(self):
        item_to_create = self.get_item_to_create()
        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create)
        self.assertEqual(401, response.status_code)

    def test_invalid_creation(self):
        item_to_create = self.get_invalid_item_to_create()
        response = self.client_api().post(self.get_base_endpoint(), json=item_to_create,
                                          headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_update(self):
        item_to_update = self.get_item_to_create()
        item_to_update["id"] = self.get_default_id()

        response = self.client_api().put(self._get_endpoint_by_id(), json=item_to_update,
                                         headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.__assert_equal_item(item_to_update, response_dto)

    def test_update_without_login(self):
        item_to_update = self.get_item_to_create()
        item_to_update["id"] = self.get_default_id()

        response = self.client_api().put(self._get_endpoint_by_id(), json=item_to_update)

        self.assertEqual(401, response.status_code)

    def test_update_from_another_user(self):
        item_to_update = self.get_item_to_create()

        response = self.client_api().put(self._get_endpoint_by_id(self.get_id_from_another_user()),
                                         json=item_to_update, headers=self.get_authentication_header())

        self.assertEqual(403, response.status_code)

    def test_invalid_update(self):
        item_to_update = self.get_invalid_item_to_create()
        item_to_update["id"] = self.get_default_id()

        response = self.client_api().put(self._get_endpoint_by_id(), json=item_to_update,
                                         headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_delete(self):
        response = self.client_api().get(self._get_endpoint_by_id(), headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto)

        response = self.client_api().delete(self._get_endpoint_by_id(), headers=self.get_authentication_header())
        self.assertEqual(204, response.status_code)

        response = self.client_api().get(self._get_endpoint_by_id(), headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNone(response_dto)

    def test_delete_without_delete(self):
        response = self.client_api().delete(self._get_endpoint_by_id())
        self.assertEqual(401, response.status_code)

    def test_delete_from_another_user(self):
        response = self.client_api().delete(self._get_endpoint_by_id(self.get_id_from_another_user()),
                                            headers=self.get_authentication_header())
        self.assertEqual(403, response.status_code)

    def __assert_equal_item(self, item_a: dict, item_b: dict):
        for key, value in item_a.items():
            if isinstance(value, dict):
                self.__assert_equal_item(value, item_b[key])
            elif isinstance(value, list):
                for index, item_from_value in enumerate(value):
                    self.__assert_equal_item(item_from_value, item_b[key][index])
            else:
                if value and item_b.get(key):
                    self.assertEqual(value, item_b[key])

    def __assert_each_item(self, item_dto: dict):
        self.assertIsNotNone(item_dto["name"])
        self.assertIsNotNone(item_dto["created_by"])
        self.assertIsNotNone(item_dto["created_at"])
        self.assertIsNotNone(item_dto["modified_at"])
