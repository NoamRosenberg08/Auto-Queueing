import json
from typing import Dict

import mss
import roboflow
from mss.base import MSSBase

import MatchNumberFinder
import MatchTimeFinder


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api: roboflow.Roboflow = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

screenshooter: MSSBase = mss.mss()


match_time_finder: MatchTimeFinder = MatchTimeFinder.MatchTimeFinder(roboflow_api, "timedetectionv2", 5, screenshooter)
match_number_finder: MatchNumberFinder = MatchNumberFinder.MatchNumberFinder(roboflow_api, "matchdetectionv2", 1, screenshooter)

print(match_number_finder.get_match_number())
while True:
    print(match_time_finder.get_match_time())
