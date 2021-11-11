from dataclasses import dataclass


@dataclass
class User(object):
    id: int
    name: str
    login: str
    password: str
