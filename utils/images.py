import sys
import random
import argparse
import imagehash
import numpy as np
import math
from PIL import Image

# http://paulbourke.net/dataformats/asciiart/
grayscale_large = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
grayscale_small = r'@%#*+=-:. '


def compare_images(image1, image2, cutoff=5):
    """
    Compares how different two different images are
    :param image1: image to compare
    :param image2: image to compare
    :param cutoff: accepted difference between images, 5 is a reasonable default.
    :return:
    """
    image1 = imagehash.average_hash(image1)
    image2 = imagehash.average_hash(image2)
    if image1 - image2 < cutoff:
        return True
    return False


def average_luminance(image: Image) -> int:
    """
    Gets the average luminance of an image
    :param image: input PIL image
    :return: average luminance
    """
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


def image_to_ascii(image: Image, columns: int = 80, scale: float = 0.43):
    """
    Converts an image to ascii art
    :param image: PIL input image
    :param columns: Columns of the output/resolution
    :param scale: Scale of the image, sensible default
    :return:
    """
    global grayscale_large, grayscale_small

    # convert to grayscale
    image = image.convert('L')

    # store dimensions
    image_width, image_height = image.size[0], image.size[1]

    width = image_width / columns
    height = width / scale
    rows = int(image_height / height)

    # check if it's actually possible to convert
    if columns > image_width or rows > image_height:
        return None

    ascii_image = ""
    for row in range(rows):
        tile1 = int(row * height)
        tile2 = int((row + 1) * height)
        if row == rows - 1:
            tile2 = image_height
        row_pixels = ""
        for i in range(columns):
            tile3 = int(i * width)
            tile4 = int((i + 1) * width)
            if i == columns - 1:
                tile4 = image_width

            final_image = image.crop((tile3, tile1, tile4, tile2))

            # find average luminance
            avg = int(average_luminance(final_image))
            grayscale_pixel = grayscale_small[int((avg * 9) / 255)]
            row_pixels += grayscale_pixel
            # add char to row
        # append row to ascii image
        ascii_image += row_pixels + "\n"
    return ascii_image
