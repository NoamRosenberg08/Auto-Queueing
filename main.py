import json
import threading
import time
from threading import Thread
from typing import Dict, List

import mss
import roboflow
from flask import Flask, jsonify, request
from mss.base import MSSBase

import FRCEventsAPIHandler
import MatchNumberFinder
import MatchTimeFinder
from flask_cors import CORS
from FRCEventsAPIHandler import FRCEventsAPIHandler
from Match import Match


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api: roboflow.Roboflow = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

match_number: int = 0
match_time: float = 0

api_username = config['FRCEvents']['username']
api_token = config['FRCEvents']['token']
print(api_token)
season_year = config['FRCEvents']['season']


def convert_match_mist_to_dict_by_number(match_list: List[Match]) ->  Dict[int, List]:
    match_dict: Dict[int, List] = {}
    for match in match_list:
        match_dict[match.number] = match.teams
    return match_dict


frc_api_handler: FRCEventsAPIHandler = FRCEventsAPIHandler(api_username, api_token, season_year)
match_dict = convert_match_mist_to_dict_by_number(frc_api_handler.get_schedule_for_team(config['event_code'],config['team_number']))

app = Flask(__name__)
CORS(app)

@staticmethod
def should_queue(current_match: int, teams_match_list: Dict[int, List], matches_before_queue: int):
    for i in range(matches_before_queue + 1):
        if current_match + i in teams_match_list.keys():
            return True
    return False

@app.route("/match")
def get_match_details():
    return jsonify({"MatchTime": match_time, "MatchNumber": match_number})

@app.route("/match/time")
def get_match_time():
    return jsonify({"MatchTime": match_time})

@app.route("/match/number")
def get_match_number():
    return jsonify({"MatchNumber": match_number})

@app.route("/schedule/team/should_queue")
def should_team_go_to_queue():
    return jsonify({'should_queue': str(should_queue(match_number, match_dict,config['matches_before_queue'])), "current_match": match_number})

@app.route("/schedule/team")
def get_schedule_for_team():
    return jsonify(match_dict)

#
# def update_match_info():
#     global match_time, match_number
#     screenshooter : MSSBase = mss.mss()
#
#     match_time_finder: MatchTimeFinder = MatchTimeFinder.MatchTimeFinder(roboflow_api, "timedetectionv2", 5, screenshooter)
#     match_number_finder: MatchNumberFinder = MatchNumberFinder.MatchNumberFinder(roboflow_api, "matchdetectionv2", 1,screenshooter)
#
#     while True:
#         screenshooter = mss.mss()
#         if match_time == 0:
#             match_number = match_number_finder.get_match_number()
#         match_time = match_time_finder.get_match_time()
#         print("Current match time:", match_time)
#         time.sleep(1)  # Sleep to avoid excessive CPU usage
#
# background_thread = threading.Thread(target=update_match_info, daemon=True)
# background_thread.start()

def run_flask():
    app.run(debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

while True:
    time.sleep(1)