from abc import ABC, abstractmethod
from typing import List, Dict
from Match import Match


class IEventAPI(ABC):

    @abstractmethod
    def get_schedule_for_event(self, event_code: str) -> List[Dict]:
        pass

    @abstractmethod
    def is_team_in_match(self, match: dict, team_number: int) -> bool:
        pass

    @abstractmethod
    def get_schedule_for_team(self,event_code: str, team_number: int) -> List[Match]:
        pass
