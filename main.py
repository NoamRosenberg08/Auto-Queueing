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


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api: roboflow.Roboflow = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

match_number: float = 0
match_time: float = 0

app = Flask(__name__)

@app.route("/")
def get():
    return jsonify({"MatchTime": match_time, "MatchNumber": match_number})

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