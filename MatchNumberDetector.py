from PIL import Image
import numpy
from numpy import ndarray

THRESHOLD : int = 120

image : Image = Image.open("C:\\Users\\control\\PycharmProjects\\Auto-Queueing\\Screenshot 2025-04-27 135818.png").convert('L')
image_array : ndarray = numpy.asarray(image)

def convert_image_to_grayscale(image_as_array : ndarray):
    return image_as_array > THRESHOLD

Image.fromarray(convert_image_to_grayscale(image_array)).show()