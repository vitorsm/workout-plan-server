import abc
from typing import Optional, List

from workout_plan_server.domain.entities.generic_entity import GenericEntity
from workout_plan_server.domain.entities.user import User
from workout_plan_server.domain.exceptions.entity_not_found_exception import EntityNotFoundException
from workout_plan_server.domain.exceptions.invalid_entity_exception import InvalidEntityException
from workout_plan_server.domain.exceptions.permission_exception import PermissionException
from workout_plan_server.services.ports.authentication_repository import AuthenticationRepository
from workout_plan_server.services.ports.entity_repository import EntityRepository


class GenericEntityService(metaclass=abc.ABCMeta):

    def __init__(self, authentication_repository: AuthenticationRepository):
        self.authentication_repository = authentication_repository

    @abc.abstractmethod
    def get_repository(self) -> EntityRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_entity_name(self) -> str:
        raise NotImplementedError

    def create(self, entity: GenericEntity) -> GenericEntity:
        self.prepare_to_persist(entity)
        self.valid_to_persist(entity, to_delete=False)

        return self.get_repository().create(entity)

    def update(self, entity: GenericEntity):
        persisted_entity = self.find_by_id(entity.id)

        if not persisted_entity:
            raise EntityNotFoundException(self.get_entity_name(), entity.id)

        GenericEntityService.__merge_persisted_entity(persisted_entity, entity)

        self.prepare_to_persist(entity)
        self.valid_to_persist(entity, to_delete=False)
        self.get_repository().update(entity)

    def delete(self, entity_id: str):
        entity = self.find_by_id(entity_id)

        if not entity:
            raise EntityNotFoundException(self.get_entity_name(), entity_id)

        self.valid_to_persist(entity, to_delete=True)

        self.get_repository().delete(entity)

    def find_by_id(self, entity_id: str) -> Optional[GenericEntity]:
        entity = self.get_repository().find_by_id(entity_id)

        if not entity:
            return None

        user = self.authentication_repository.get_current_user()
        GenericEntityService.__assert_entity_user(entity, user)

        return entity

    def find_all_by_ids(self, entity_ids: List[str]) -> List[GenericEntity]:
        entities = self.get_repository().find_all_by_ids(entity_ids)

        if not entities:
            return entities

        user = self.authentication_repository.get_current_user()
        for entity in entities:
            GenericEntityService.__assert_entity_user(entity, user)

        return entities

    def find_all_by_user(self) -> List[GenericEntity]:
        user = self.authentication_repository.get_current_user()
        return self.get_repository().find_all_by_user(user)

    def valid_required_fields(self, entity: GenericEntity):
        missing_fields = entity.get_missing_fields()

        if missing_fields:
            raise InvalidEntityException(self.get_entity_name(), missing_fields)

    def prepare_to_persist(self, entity: GenericEntity):
        if not entity:
            return

        user = self.authentication_repository.get_current_user()
        entity.fill_track(user)

    def valid_to_persist(self, entity: GenericEntity, to_delete: bool):
        if not entity:
            raise InvalidEntityException(self.get_entity_name(), list())

        user = self.authentication_repository.get_current_user()

        GenericEntityService.__assert_entity_user(entity, user)

        if not to_delete:
            self.valid_required_fields(entity)

    @staticmethod
    def __merge_persisted_entity(persisted_entity: GenericEntity, entity: GenericEntity):
        if not persisted_entity:
            return

        entity.id = persisted_entity.id
        entity.created_at = persisted_entity.created_at
        entity.modified_at = persisted_entity.modified_at
        entity.created_by = persisted_entity.created_by

    @staticmethod
    def __assert_entity_user(entity: GenericEntity, user: User):
        if entity.created_by != user:
            raise PermissionException("You cant change data from others users")
