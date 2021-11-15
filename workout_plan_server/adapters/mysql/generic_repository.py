from typing import TypeVar, Generic, List

from sqlalchemy.exc import IntegrityError

from workout_plan_server.adapters.utils import sql_utils
from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException

Entity = TypeVar("Entity")


class GenericRepository(Generic[Entity]):
    def __init__(self, db):
        self.db = db

    def commit(self, raise_integrity_error: bool = False):
        try:
            self.db.session.commit()
        except IntegrityError as ex:
            if raise_integrity_error:
                raise ex
            else:
                self.__handle_integrity_error(ex, "")

    def add(self, entity: object, commit: bool = False):
        self.db.session.add(entity)
        if commit:
            try:
                self.commit(raise_integrity_error=True)
            except IntegrityError as ex:
                self.__handle_integrity_error(ex, type(entity).__name__)

    def update(self, entity: object, commit: bool = False):
        if entity not in self.db.session:
            self.db.session.add(entity)
        if commit:
            self.db.session.commit()

    def delete(self, entity: object, commit: bool = False):
        self.db.session.delete(entity)
        if commit:
            self.commit()

    def find_by_user(self, user: User) -> List[Entity]:
        return self.db.session.query(Entity).filter(Entity.created_by == user).all()

    @staticmethod
    def __handle_integrity_error(exception: IntegrityError, entity: str):
        if "UNIQUE" in exception.args[0] or "Duplicate" in exception.args[0]:
            if "UNIQUE" in exception.args[0]:
                field = exception.args[0].split(': ')[1]
            else:
                field = exception.args[0].split('\' for key \'')[1][:-3].split('.')[1]
            value = None

            if "." in field:
                field = field.split(".")[1]

            index = sql_utils.get_position_of_field_in_insert_query(exception.statement, field)

            if exception.params and len(exception.params) > index >= 0:
                if type(exception.params) == list or type(exception.params) == tuple:
                    value = exception.params[index]
                else:
                    value = exception.params[field]

            raise DuplicateEntityException(entity, field, value)

        raise exception
