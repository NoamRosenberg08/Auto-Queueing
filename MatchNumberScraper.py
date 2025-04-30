from time import sleep
from typing import Dict

import cv2
import mss
from PIL import Image, ImageFilter,ImageEnhance
import numpy
from numpy import ndarray
from mss.base import MSSBase

import ScreenShotUtils
import pyautogui

THRESHOLD: int = 60

REGION = {
    "top": 255,

    "left": 1280,
    "width": 50,
    "height": 27
}

# image: Image = Image.open(
#     "C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\Screenshot 2025-04-27 135818.png").convert('L')
# image_array: ndarray = numpy.asarray(image)


def convert_image_to_binary(image: Image) -> Image:
    return Image.fromarray(numpy.asarray(image) > THRESHOLD)

def resize_image(image: Image ,times: float=1) -> Image:
    return image.resize((image.width * times, image.height * times), Image.LANCZOS)

def enhance_image_contrast(image: Image, enhancement_factor: float):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(enhancement_factor)

def screenshot_match_number(screenshooter: MSSBase):
    return ScreenShotUtils.grab_screenshot(screenshooter, REGION)


screenshooter = mss.mss()

def capture_all_match_numbers():
    sleep(5)
    for i in range(75):
        sleep(3)
        print(f"capturing match {i}")
        cv2img = screenshot_match_number(screenshooter=screenshooter)
        cv2.imwrite(f"match_number{i}.png", cv2img)
        pyautogui.hotkey("shift", "n")

def convert_all_match_numbers_images_to_grayscale():
    for i in range(75):
        grayscale_image : Image = Image.open(f"C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\match_number{i}.png").convert('L')
        binary_image : ndarray = convert_image_to_binary(numpy.asarray(grayscale_image))
        Image.fromarray(binary_image).save(f"binary_match_number{i}.png")


def enhance_image(image: Image) -> Image:
    return enhance_image_contrast(resize_image(image.convert('L'), 30),3)

def enhance_images():
    for i in range(75):
        image: Image = Image.open(f"C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\match_number{i}.png").convert('L')
        enhance_image(image).save(f"enhanced_image{i}.png")



# Image.fromarray(convert_image_to_binary(numpy.asarray(Image.open("C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\Screenshot 2025-04-30 140137.png").convert('L')))).save("grayscale.png")