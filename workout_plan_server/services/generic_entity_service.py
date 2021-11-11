import abc
from typing import TypeVar, Generic, Optional

from workout_plan_server.domain.entities.generic_entity import GenericEntity
from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.ports.entity_repository import EntityRepository
from workout_plan_server.application.utils import authentication_utils

Entity = TypeVar("Entity", bound=GenericEntity)


class GenericEntityService(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_repository(self) -> EntityRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def valid_required_fields(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_entity_name(self) -> str:
        raise NotImplementedError

    def create(self, entity: Entity) -> Entity:
        GenericEntityService.__prepare_to_persist(entity)
        self.__valid_to_persist(entity, to_delete=False)

        return self.get_repository().create(entity)

    def update(self, entity: Entity):
        GenericEntityService.__prepare_to_persist(entity)
        self.__valid_to_persist(entity, to_delete=False)
        self.get_repository().update(entity)

    def delete(self, entity_id: str):
        entity = self.find_by_id(entity_id)

        if not entity:
            raise EntityNotFoundException(self.get_entity_name(), entity_id)

        self.__valid_to_persist(entity, to_delete=True)

        self.get_repository().delete(entity)

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        user = authentication_utils.get_current_user()

        entity = self.get_repository().find_by_id(entity_id)
        GenericEntityService.__assert_entity_user(entity, user)

        return entity

    @staticmethod
    def __prepare_to_persist(entity: Entity):
        user = authentication_utils.get_current_user()
        entity.fill_track(user)

    def __valid_to_persist(self, entity: Entity, to_delete: bool):
        user = authentication_utils.get_current_user()

        GenericEntityService.__assert_entity_user(entity, user)

        if not to_delete:
            self.valid_required_fields(entity)

    @staticmethod
    def __assert_entity_user(entity: Entity, user: User):
        if entity.created_by != user:
            raise PermissionException("You cant change data from others users")
