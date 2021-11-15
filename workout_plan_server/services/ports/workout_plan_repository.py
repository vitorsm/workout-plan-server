import abc

from workout_plan_server.domain.entities.workout_plan import WorkoutPlan
from workout_plan_server.services.ports.entity_repository import EntityRepository


class WorkoutPlanRepository(EntityRepository[WorkoutPlan], metaclass=abc.ABCMeta):
    pass
