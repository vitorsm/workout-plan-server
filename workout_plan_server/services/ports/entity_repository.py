import abc
from typing import Optional, Type, TypeVar, Generic

from workout_plan_server.domain.entities.generic_entity import GenericEntity

Entity = TypeVar("Entity", bound=GenericEntity)


class EntityRepository(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, entity: GenericEntity) -> GenericEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, entity: GenericEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: GenericEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[GenericEntity]:
        raise NotImplementedError
