from time import sleep

import cv2
import mss
import numpy as np
from PIL import Image
from mss.base import MSSBase
import json
import roboflow
from roboflow import Project
from typing import List, Dict, Tuple

from roboflow.models.inference import InferenceModel

import ResultNumber
from ScreenShotUtils import grab_screenshot


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))

def get_results_from_image(model, path: str, confidence: float = 90, overlap: float = 20):
    return model.predict(path, confidence=confidence, overlap=overlap)

def results_to_result_numbers(results : List[ResultNumber]) -> List[ResultNumber]:
    results_list: List[ResultNumber] = []
    for result in results:
        results_list.append(ResultNumber.ResultNumber(int(result['class']), result['x'], result['y']))
    return results_list

def sort_numbered_results_list_by_x_value(numbered_results : List[ResultNumber]) -> List[ResultNumber]:
    return sorted(numbered_results, key=lambda result: result.x)

def convert_numbered_to_time_in_seconds(numbered_results: List[ResultNumber]) -> int:

    if len(numbered_results) != 3:
        return -1

    return (numbered_results[0].number * 60) + (numbered_results[1].number * 10) + numbered_results[2].number

REGION = {
    "top": 270,
    "left": 1250,
    "width": 65,
    "height": 40
}

result: List[Dict] = get_results_from_image(model,'C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png')
numbered_results : List[ResultNumber] = results_to_result_numbers(result)

# while True:
#     img: Image = grab_screenshot(screenshooter=screenshooter, region=region)
#     img.save("current_screen.png")
#     result: List[Dict] = get_results_from_image(model, 'C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png')
#     numbered_results: List[ResultNumber] = results_to_result_numbers(result)
#
#     time = convert_numbered_to_time_in_seconds(sort_numbered_results_list_by_x_value(numbered_results))
#     print(time)

class MatchTimeFinder:
    def __init__(self, roboflow_api: roboflow.Roboflow, project_name: str, model_version: int, screenshooter: MSSBase):
        self.project: Project = roboflow_api.workspace().project(project_name)
        self.model : InferenceModel = self.project.version(model_version).model
        self.screenshooter = screenshooter

    def get_match_time(self):
        grab_screenshot(screenshooter=self.screenshooter, region=REGION).save("current_screen.png")
        result: List[Dict] = get_results_from_image(self.model, 'C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png')
        numbered_results: List[ResultNumber] = results_to_result_numbers(result)

        return convert_numbered_to_time_in_seconds(sort_numbered_results_list_by_x_value(numbered_results))