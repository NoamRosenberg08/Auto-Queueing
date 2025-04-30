import json
from typing import Dict, List

import roboflow
from roboflow import Project, Roboflow

from PIL import Image
from mss.base import MSSBase
from roboflow.models.inference import InferenceModel

import ImageUtils
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


class MatchNumberFinder:

    def __init__(self,  roboflow_api: Roboflow, project_name: str,  model_version: int):
        self.project: Project = roboflow_api.workspace().project(project_name)
        self.model : InferenceModel = self.project.version(model_version).model

    def periodic(self, screenshooter: MSSBase):
        enhance_image(screenshot_match_number(screenshooter, REGION)).show()

    def detect_numbers(self, image_path: str) -> List[Dict]:
        return self.model.predict(image_path, confidence=50, overlap=20)



config = json.load(open('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json','r'))
roboflow_api = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

finder = MatchNumberFinder(roboflow_api, "matchdetectionv2", 1)
print(str(finder.detect_numbers('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\enhancedimages\\enhanced_image38.png')))




