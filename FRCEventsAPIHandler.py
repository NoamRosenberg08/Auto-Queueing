from typing import Dict

import requests


def request_data(headers: Dict, endpoint: str, payload: str):
    return requests.request("GET", endpoint, headers=headers, data=payload)


class FRCEventsAPIHandler:

    def __init__(self):
        pass

    def get_qual_list(self, event_code: str, team_number: int):
        return {
            1: {'red': {4590, 2222, 1111}, 'blue': {3333, 4444, 5555}},
            10: {'red': {2222, 1111, 4590}, 'blue': {3333, 4444, 5555}},
            20: {'red': {4444, 2222, 1111}, 'blue': {3333, 4590, 5555}},
            30: {'red': {2222, 3333, 1111}, 'blue': {4590, 4444, 5555}},
            35: {'red': {5555, 2222, 1111}, 'blue': {3333, 4444, 4590}},
            40: {'red': {4590, 2222, 1111}, 'blue': {3333, 4444, 5555}},
            45: {'red': {2222, 1111, 4590}, 'blue': {3333, 4444, 5555}},
            50: {'red': {4444, 2222, 1111}, 'blue': {3333, 4590, 5555}},
            60: {'red': {2222, 3333, 1111}, 'blue': {4590, 4444, 5555}},
            70: {'red': {5555, 2222, 1111}, 'blue': {3333, 4444, 4590}}
        }
