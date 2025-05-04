from enum import Enum

import requests
from typing import Dict, List
import json
import base64

"""
Disctrict Codes:

FMA
PNW
NE
FIN
FNC
ONT
ISR
CHS
FIT
PCH
FIM
"""


@staticmethod
def encode_credentials(username: str, token: str):
    return base64.b64encode((username + ":" + token).encode('ascii')).decode('ascii')

class FRCEventsAPIHandler:
    def __init__(self, api_username: str, api_token: str, season_year: int):
        self.base_url = "https://frc-api.firstinspires.org/v3.0/" + str(season_year) + "/"
        self.headers = {
            'Authorization': "Basic " + encode_credentials(username=api_username, token=api_token),
            'If-Modified-Since': ''
        }

        print("FRCEventsAPIHandler initialized with base URL: " + self.base_url)

    def get_request(self, endpoint: str):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_event_list(self, district_code: str = None) -> Dict:
        event_code_list: Dict = {}
        for event in self.get_request(f"events?districtCode={district_code}")['Events']:
            event_code_list[event['code']] = event
        return event_code_list

    def get_schedule_for_event(self, event_code: str) -> List[Dict]:
        '''

        :param event_code:
        :return: List[Dict] every element of the list is data about this specific match.
        note that list[0] = qual 1
        '''

        url = f"schedule/{event_code}?tournamentLevel=Qualification"
        return self.get_request(url)['Schedule']


    def is_team_in_match(self, match: dict, team_number: int):
        for team in match['teams']:
            if team['teamNumber'] == team_number:
                return True
        return False

    def get_schedule_for_team(self, schedule : List[Dict], team_number: int) -> List[Dict]:
        '''

        :param schedule:
        :param team_number:
        :return: List[Dict] - every element of the list is a match. List[0] = qual 1
        '''
        teams_schedule: List[Dict] = []

        for match in schedule:
            if self.is_team_in_match(match, team_number):
                teams_schedule.append(match)
        return teams_schedule

if __name__ == "__main__":
    # Example usage
    # use the config.json file to get the api username and token
    with open('config.json') as config_file:
        config = json.load(config_file)
        api_username = config['FRCEvents']['username']
        api_token = config['FRCEvents']['token']
        print(api_token)
    season_year = 2025

    frc_api_handler = FRCEventsAPIHandler(api_username, api_token, season_year)
    events = frc_api_handler.get_event_list("ISR")
    # print(events)
    schdule = frc_api_handler.get_schedule_for_event('ISCMP')
    # print(schdule)
    print(frc_api_handler.get_schedule_for_team(schdule, 4590))
