from dataclasses import dataclass


@dataclass
class User(object):
    id: str
    name: str
    login: str
    password: str

    def __eq__(self, other):
        return other and other.id == self.id
