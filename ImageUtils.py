import numpy
from PIL import Image, ImageEnhance


def convert_image_to_binary(image: Image, threshold: float) -> Image:
    return Image.fromarray(numpy.asarray(image) > threshold)

def resize_image(image: Image ,times: float=1) -> Image:
    return image.resize((image.width * times, image.height * times), Image.LANCZOS)

def enhance_image_contrast(image: Image, enhancement_factor: float) -> Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(enhancement_factor)