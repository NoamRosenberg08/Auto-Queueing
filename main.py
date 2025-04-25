from typing import Dict
import cv2
import mss
import numpy as np
from PIL import Image, ImageDraw
from mss.base import MSSBase
import json
import roboflow
from roboflow import Project


def load_json(path: str) -> Dict:
    return json.load(open(path, 'r'))

def grab_screenshot(screenshooter: MSSBase, region: Dict = None) -> np.ndarray:
    if region is None:
        screenshot = screenshooter.grab(screenshooter.monitors[1])
    else:
        screenshot = screenshooter.grab(region)
    return np.array(screenshot)

def get_results_from_image(model, path: str, confidence: float = 80, overlap: float = 20):
    return model.predict(path, confidence=confidence, overlap=overlap)


config = load_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')
roboflow_api = roboflow.Roboflow(api_key=config['roboflow']['api_key'])

project: Project = roboflow_api.workspace().project('timedetectionv2')
model = project.version(4).model


screenshooter = mss.mss()

region = {
    "top": 270,
    "left": 1250,
    "width": 70,
    "height": 50
}
#
# img = grab_screenshot(screenshooter=screenshooter, region=region)
# cv2.imwrite("current_screen.png", img)
img = Image.open("C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png")

print(get_results_from_image(model,'C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png'))
img.show()















