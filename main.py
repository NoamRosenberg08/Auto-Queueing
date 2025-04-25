from typing import Dict
import cv2
import mss
import numpy as np
from PIL import Image
from mss.base import MSSBase
import json

def load_credentials_json(path: str):
    return json.load(open(path, 'r'))

def grab_screenshot(screenshooter: MSSBase, region: Dict = None) -> np.ndarray:
    if region is None:
        screenshot = screenshooter.grab(screenshooter.monitors[1])
    else:
        screenshot = screenshooter.grab(region)
    return np.array(screenshot)


screenshooter = mss.mss()

region = {
    "top": 270,
    "left": 1250,
    "width": 70,
    "height": 50
}

img = grab_screenshot(screenshooter=screenshooter, region=region)
cv2.imwrite("current_screen.png", img)
img = Image.open("C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\current_screen.png")

print(load_credentials_json('C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\config.json')['api_key'])


img.show()
