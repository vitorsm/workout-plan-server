import json

from tests.integration_tests.base_test import BaseTest


class TestUserController(BaseTest):

    def test_get_current_user(self):
        response = self.client.get(f"/v1/user/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Admin", response_dto["name"])
        self.assertEqual("admin", response_dto["login"])

    def test_create_user(self):
        user_dto = {
            "login": "test1",
            "name": "Test1",
            "password": "12345"
        }

        response = self.client.post(f"/v1/user/", json=user_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["id"])
        self.assertEqual(user_dto["name"], response_dto["name"])
        self.assertEqual(user_dto["login"], response_dto["login"])

    def test_create_user_duplicate(self):
        user_dto = {
            "login": "admin",
            "name": "Test1",
            "password": "12345"
        }

        response = self.client.post(f"/v1/user/", json=user_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(409, response.status_code)
        self.assertEqual("DuplicateEntityException", response_dto["type"])

    def test_create_invalid_user(self):
        user_dto = {
            "login": "",
            "name": "",
            "password": ""
        }

        response = self.client.post(f"/v1/user/", json=user_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_update_user(self):
        user_dto = {
            "login": "admin1",
            "name": "Test1",
            "password": "12345"
        }

        response = self.client.put(f"/v1/user/{self.default_id}", json=user_dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.default_id, response_dto["id"])
        self.assertEqual(user_dto["name"], response_dto["name"])
        self.assertEqual(user_dto["login"], response_dto["login"])

    def test_update_invalid_user(self):
        user_dto = {
            "login": "",
            "name": "",
            "password": ""
        }

        response = self.client.put(f"/v1/user/{self.default_id}", json=user_dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual("InvalidEntityException", response_dto["type"])

    def test_update_without_permission(self):
        user_dto = {
            "login": "admin1",
            "name": "Test1",
            "password": "12345"
        }

        response = self.client.put(f"/v1/user/{self.secondary_default_id}", json=user_dto,
                                   headers=self.get_authentication_header())

        self.assertEqual(403, response.status_code)

    def test_update_duplicate_user(self):
        user_dto = {
            "login": "user2",
            "name": "Test1",
            "password": "12345"
        }

        response = self.client.put(f"/v1/user/{self.default_id}", json=user_dto,
                                   headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(409, response.status_code)
        self.assertEqual("DuplicateEntityException", response_dto["type"])

    def test_authenticate_success(self):
        login_dto = {
            "username": "admin",
            "password": "user1"
        }

        response = self.client.post(f"/v1/auth/authenticate", json=login_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["access_token"])

    def test_create_update_and_authenticate_success(self):
        user_dto = {
            "login": "user",
            "password": "user",
            "name": "User"
        }

        # Creating user
        response = self.client.post(f"/v1/user/", json=user_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)

        user_id = response_dto["id"]

        login_dto = {
            "username": "user",
            "password": "user"
        }

        # Testing login
        response = self.client.post(f"/v1/auth/authenticate", json=login_dto)
        response_dto = json.loads(response.data.decode())
        token = response_dto["access_token"]
        header = {"Authorization": f"JWT {token}"}

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(token)

        # Testing update user
        user_dto["name"] = "User1"
        response = self.client.put(f"/v1/user/{user_id}", json=user_dto, headers=header)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(user_dto["name"], response_dto["name"])

        # Testing login after update user without change password
        response = self.client.post(f"/v1/auth/authenticate", json=login_dto, headers=header)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["access_token"])

        # Updating password
        user_dto["password"] = "user1"
        response = self.client.put(f"/v1/user/{user_id}", json=user_dto, headers=header)

        self.assertEqual(200, response.status_code)

        # Testing new password in login
        login_dto["password"] = "user1"
        response = self.client.post(f"/v1/auth/authenticate", json=login_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["access_token"])

    def test_authenticate_invalid_credentials(self):
        login_dto = {
            "username": "admin",
            "password": "user"
        }

        response = self.client.post(f"/v1/auth/authenticate", json=login_dto)

        self.assertEqual(401, response.status_code)
