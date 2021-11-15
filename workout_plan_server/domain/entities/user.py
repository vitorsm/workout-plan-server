from dataclasses import dataclass
from typing import List


@dataclass
class User(object):
    id: str
    name: str
    login: str
    password: str

    def __eq__(self, other):
        return other and other.id == self.id

    def get_missing_fields(self, is_create: bool) -> List[str]:
        missing_fields = list()

        if not self.name:
            missing_fields.append("name")
        if not self.login:
            missing_fields.append("login")
        if is_create and not self.password:
            missing_fields.append("password")

        return missing_fields
