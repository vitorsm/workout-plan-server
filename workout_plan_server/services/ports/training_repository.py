import abc
from workout_plan_server.domain.entities.training import Training
from workout_plan_server.services.ports.entity_repository import EntityRepository


class TrainingRepository(EntityRepository[Training], metaclass=abc.ABCMeta):
    pass
