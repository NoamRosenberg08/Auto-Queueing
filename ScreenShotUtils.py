from mss.base import MSSBase
from typing import Dict
import numpy as np

def grab_screenshot(screenshooter: MSSBase, region: Dict = None) -> np.ndarray:
    if region is None:
        screenshot = screenshooter.grab(screenshooter.monitors[1])
    else:
        screenshot = screenshooter.grab(region)
    return np.array(screenshot)
