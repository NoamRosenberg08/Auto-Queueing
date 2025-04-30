from PIL import Image
from mss.base import MSSBase
from typing import Dict
import numpy as np

def grab_screenshot(screenshooter: MSSBase, region: Dict = None) -> Image:
    if region is None:
        screenshot = screenshooter.grab(screenshooter.monitors[1])
    else:
        screenshot = screenshooter.grab(region)
    return Image.fromarray(np.array(screenshot))
