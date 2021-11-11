import abc

from workout_plan_server.domain.entities.exercise import Exercise
from workout_plan_server.services.ports.entity_repository import EntityRepository


class ExerciseRepository(EntityRepository[Exercise], metaclass=abc.ABCMeta):
    pass
