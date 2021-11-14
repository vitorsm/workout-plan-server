
from flask_restx import fields


user_dto = {
    "id": fields.String(readOnly=True, description="User id"),
    "name": fields.String(required=True, description="User name"),
    "login": fields.String(required=True, description="User login"),
    "password": fields.String(required=True, description="User password")
}
