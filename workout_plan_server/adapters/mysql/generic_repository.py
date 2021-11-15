from typing import TypeVar, Generic, List, Optional
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeMeta

from workout_plan_server.adapters.utils import sql_utils
from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.duplicate_entity_exception import DuplicateEntityException

Entity = TypeVar("Entity")


class GenericRepository(Generic[Entity]):
    def __init__(self, db: SQLAlchemy, entity_type: DeclarativeMeta):
        self.db = db
        self.entity_type = entity_type

    def commit(self, raise_integrity_error: bool = False):
        try:
            self.db.session.commit()
        except IntegrityError as ex:
            if raise_integrity_error:
                raise ex
            else:
                self.__handle_integrity_error(ex, "")

    def create(self, entity: Entity, commit: bool = True) -> Entity:
        model = self.entity_type.from_entity(entity)
        model.id = str(uuid4())

        self.db.session.add(model)
        if commit:
            try:
                self.commit(raise_integrity_error=True)
            except IntegrityError as ex:
                self.__handle_integrity_error(ex, type(entity).__name__)

        return model.to_entity()

    def update(self, entity: object, commit: bool = True):
        model = self.entity_type.from_entity(entity)

        self.db.session.merge(model)
        if commit:
            self.db.session.commit()

    def delete(self, entity: object, commit: bool = True):
        self.db.session.query(self.entity_type).filter(self.entity_type.id == entity.id).delete()
        if commit:
            self.commit()

    def find_all_by_user(self, user: User) -> List[Entity]:
        models = self.db.session.query(self.entity_type).filter(self.entity_type.created_by_id == user.id).all()
        return [model.to_entity() for model in models]

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        model = self.db.session.query(self.entity_type).filter(self.entity_type.id == entity_id).first()

        if not model:
            return None

        return model.to_entity()

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
