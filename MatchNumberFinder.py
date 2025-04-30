import json
from typing import Dict, List

import mss
import roboflow
from roboflow import Project, Roboflow

from PIL import Image
from mss.base import MSSBase
from roboflow.models.inference import InferenceModel

import ImageUtils
import ResultNumber
import ScreenShotUtils

REGION = {
    "top": 255,
    "left": 1280,
    "width": 50,
    "height": 27
}

THRESHOLD: float = 60
SCALING_FACTOR: float = 30
ENHANCEMENT_FACTOR: float = 3

def screenshot_match_number(screenshooter: MSSBase, region: Dict) -> Image:
    return ScreenShotUtils.grab_screenshot(screenshooter, region)


def enhance_image(image: Image) -> Image:
    return ImageUtils.enhance_image_contrast(ImageUtils.resize_image(image.convert('L'), SCALING_FACTOR),ENHANCEMENT_FACTOR)

def convert_detection_numbered_results(detections: List[Dict]) -> List[ResultNumber]:
    resulted_number_list = []
    for detection in detections:
        resulted_number_list.append(ResultNumber.ResultNumber(detection['class'], detection['x'], detection['y']))
    return resulted_number_list

def convert_result_number_list_to_number(resulted_number_list: List[ResultNumber]) -> int:
    number: int = 0
    counter: int = 0
    for resulted_number in resulted_number_list:
        number += int(resulted_number.number * (10 ** counter))

    return number

class MatchNumberFinder:

    def __init__(self,  roboflow_api: Roboflow, project_name: str,  model_version: int, screenshooter: MSSBase):
        self.project: Project = roboflow_api.workspace().project(project_name)
        self.model : InferenceModel = self.project.version(model_version).model
        self.screenshooter = screenshooter

    def get_match_number(self):
        enhance_image(screenshot_match_number(self.screenshooter, REGION)).save("current_match_e.png")
        detection = self.detect_numbers('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_match_e.png')
        numbered_result_list : List[ResultNumber] = convert_detection_numbered_results(detection)
        print(numbered_result_list)
        print(convert_result_number_list_to_number(numbered_result_list))

    def detect_numbers(self, image_path: str) -> List[Dict]:
        return self.model.predict(image_path, confidence=50, overlap=20)




config = json.load(open('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json','r'))
roboflow_api = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

finder = MatchNumberFinder(roboflow_api, "matchdetectionv2", 1, mss.mss())
finder.get_match_number()



