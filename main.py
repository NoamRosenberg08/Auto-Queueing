import json
import threading
import time
from threading import Thread
from typing import Dict

import mss
import roboflow
from flask import Flask, jsonify
from mss.base import MSSBase

import MatchNumberFinder
import MatchTimeFinder
from FRCEventsAPIHandler import FRCEventsAPIHandler


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api: roboflow.Roboflow = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

match_number: float = 0
match_time: float = 0

api_username = config['FRCEvents']['username']
api_token = config['FRCEvents']['token']
print(api_token)
season_year = config['FRCEvents']['season']

frc_api_handler: FRCEventsAPIHandler = FRCEventsAPIHandler(api_username, api_token, season_year)
print(frc_api_handler)
app = Flask(__name__)

@app.route("/match")
def get_match_details():
    return jsonify({"MatchTime": match_time, "MatchNumber": match_number})

@app.route("/match/time")
def get_match_time():
    return jsonify({"MatchTime": match_time})

@app.route("/match/number")
def get_match_number():
    return jsonify({"MatchNumber": match_number})

@app.route("/schedule/team")
def get_schedule_for_team():
    return jsonify(frc_api_handler.get_schedule_for_team(config['event_code'],config['team_number']))

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