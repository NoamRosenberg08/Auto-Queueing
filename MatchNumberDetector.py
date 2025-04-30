from time import sleep
from typing import Dict

import cv2
import mss
from PIL import Image
import numpy
from numpy import ndarray
from mss.base import MSSBase

import ScreenShotUtils
import pyautogui

THRESHOLD: int = 120

REGION = {
    "top": 255,
    "left": 1280,
    "width": 100,
    "height": 27
}

image: Image = Image.open(
    "C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\Screenshot 2025-04-27 135818.png").convert('L')
image_array: ndarray = numpy.asarray(image)


def convert_image_to_grayscale(image_as_array: ndarray):
    return image_as_array > THRESHOLD


def screenshot_match_number(screenshooter: MSSBase):
    return ScreenShotUtils.grab_screenshot(screenshooter, REGION)


screenshooter = mss.mss()

sleep(5)
for i in range(10):
    sleep(4)
    print(f"capturing match {i}")
    cv2img = screenshot_match_number(screenshooter=screenshooter)
    cv2.imwrite(f"match_number{i}.png", cv2img)
    pyautogui.hotkey("shift","n")