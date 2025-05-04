from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Match:
    number: int
    teams: List[int]