from typing import Dict
import cv2
import mss
import numpy as np
from PIL import Image
from mss.base import MSSBase


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
img.show()
