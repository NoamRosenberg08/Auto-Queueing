from typing import List, Dict

import requests

from APIs.IEventAPI import IEventAPI
from Match import Match


class TBAAPI(IEventAPI):

    def __init__(self, api_token):
        self.base_url = 'https://www.thebluealliance.com/api/v3'
        self.headers = {"X-TBA-Auth-Key": api_token}

    def get_request(self, endpoint: str):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_schedule_for_event(self, event_code: str) -> List[Dict]:
        print(self.get_request(f'/event/{event_code}/matches'))
        pass

    def is_team_in_match(self, match: dict, team_number: int) -> bool:
        pass

    def get_schedule_for_team(self, event_code: str, team_number: int) -> List[Match]:
        pass

if __name__ == '__main__':
    a = TBAAPI("QXTOPyv1XGVzfOY1Bo4WJbUcdINDgND1fCJXvde4eiA8k5Fy0WsOIyQ8GRFP6AfB")
    a.get_schedule_for_event("2025iscmp")