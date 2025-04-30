from typing import Dict

import mss
from PIL import Image
from mss.base import MSSBase
from urllib3.fields import RequestField

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

    def __init__(self, api_key: str,workspace: str,project,  model_version: int):

        pass

    def periodic(screenshooter: MSSBase):
        enhance_image(screenshot_match_number(screenshooter, REGION)).show()








