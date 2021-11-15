

class InvalidCredentialsException(Exception):
    def __init__(self, login: str):
        super().__init__(f"Invalid user credentials - login: {login}")
