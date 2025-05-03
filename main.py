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


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api: roboflow.Roboflow = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

match_number: int = 0
match_time: float = 0


frc_events_api = FRCEventsAPIHandler.FRCEventsAPIHandler()
team_qual_list = frc_events_api.get_qual_list("aaa", 4590)
app = Flask(__name__)

@staticmethod
def should_queue(current_match: int, teams_match_list: List[int], matches_before_queue: int):
    # return  current_match + 2 in teams_match_list or current_match + 1 in teams_match_list or current_match in teams_match_list
    for i in range(matches_before_queue + 1):
        if current_match + i in teams_match_list:
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

@app.route("/team/qual_list")
def get_qual_list():
    return jsonify(str(frc_events_api.get_qual_list("iscmp", 49590)))

@app.route("/team/should_queue")
def should_team_go_to_queue():
    return jsonify({'should_queue': should_queue(match_number, team_qual_list.keys(), 2), "current_match": match_number})


def update_match_info():
    global match_time, match_number
    screenshooter : MSSBase = mss.mss()

    match_time_finder: MatchTimeFinder = MatchTimeFinder.MatchTimeFinder(roboflow_api, "timedetectionv2", 5, screenshooter)
    match_number_finder: MatchNumberFinder = MatchNumberFinder.MatchNumberFinder(roboflow_api, "matchdetectionv2", 1,screenshooter)

    while True:
        screenshooter = mss.mss()
        if match_time == 0:
            match_number = match_number_finder.get_match_number()
        match_time = match_time_finder.get_match_time()
        print("Current match time:", match_time)
        time.sleep(1)  # Sleep to avoid excessive CPU usage

background_thread = threading.Thread(target=update_match_info, daemon=True)
background_thread.start()

def run_flask():
    app.run(debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

while True:
    time.sleep(1)