from enum import Enum

import requests
from typing import Dict, List
import json
import base64

from flask import jsonify

from Match import Match

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


def encode_credentials(username: str, token: str):
    return base64.b64encode((username + ":" + token).encode('ascii')).decode('ascii')

def convert_schedule_to_dict(teams_schedule : List[Match]):
    schedule_dict : Dict[Match] = {}

    for match in teams_schedule:
        schedule_dict[match.number] = match.teams
    return schedule_dict

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

    def extract_teams_for_match(self, match: Dict):
        teams : List[int] = []
        for team in match['teams']:
            teams.append(team['teamNumber'])
        return teams

    def filter_teams_schedule(self, teams_schedule : List[Dict]):
        filtered_schedule: List[Match] = []

        for match in teams_schedule:
            filtered_schedule.append(Match(match['matchNumber'], self.extract_teams_for_match(match)))
        return filtered_schedule

    def get_schedule_for_team(self,event_code: str, team_number: int) -> List[Match]:
        '''

        :param event_code:
        :param team_number:
        :return: List[Dict] - every element of the list is a match. List[0] = qual 1
        '''
        schedule: List[Dict] = self.get_schedule_for_event(event_code)
        teams_schedule: List[Dict] = []

        for match in schedule:
            if self.is_team_in_match(match, team_number):
                teams_schedule.append(match)
        return self.filter_teams_schedule(teams_schedule)