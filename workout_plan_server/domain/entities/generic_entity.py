import abc
from datetime import datetime
from typing import Optional, List

from workout_plan_server.domain.entities.user import User


class GenericEntity(metaclass=abc.ABCMeta):
    id: str
    name: str

    created_by: User
    created_at: datetime
    modified_at: datetime

    @abc.abstractmethod
    def get_missing_fields(self) -> List[str]:
        raise NotImplementedError

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def fill_track(self, user: User, curr_date: Optional[datetime] = None):
        if not curr_date:
            curr_date = datetime.now()

        self.modified_at = curr_date

        if self.id:
            return

        self.created_by = user
        self.created_at = curr_date
