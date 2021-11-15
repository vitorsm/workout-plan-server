from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declared_attr

from workout_plan_server.domain.entities.generic_entity import GenericEntity

# this import ensure that userModel will be imported before use of created_by
from workout_plan_server.adapters.mysql.models.user_model import UserModel


class GenericModel(object):
    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def created_by_id(self):
        return Column(String, ForeignKey("user.id"), nullable=False)

    @declared_attr
    def created_by(self):
        return relationship("UserModel", lazy="select")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def generic_from_entity(self, entity: GenericEntity):
        self.id = entity.id
        self.name = entity.name
        self.created_at = entity.created_at
        self.modified_at = entity.modified_at
        self.created_by_id = entity.created_by.id

    def fill_generic_entity(self, entity: GenericEntity, fetch_created_by: bool = True):
        entity.id = self.id
        entity.name = self.name
        entity.created_at = self.created_at
        entity.modified_at = self.modified_at

        if fetch_created_by:
            entity.created_by = self.created_by.to_entity()

        return entity
