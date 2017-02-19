"""
use open pixel control to send the black body radiation video to whatever port.
"""

import sys
import time

import numpy as np

from led_stuff import black_body
from led_stuff import opc


def flat_pixels(temp, num_pixels=64):
    """
    return a flat array all one color, given temperature
    """
    xy_color = black_body.spline_approximation(temp)
    xyz_triple = np.asarray(black_body.xy_to_cie_xyz(*xy_color))
    xyz_image = np.ones((num_pixels, 1, 3)) * xyz_triple.reshape(1, 1, 3)
    rgb = black_body.xyz_to_rgb(xyz_image) * 255
    return rgb.reshape(num_pixels, 3)

def main(port=7890, sleep=0.001, brightness=0.3):
    """
    do the damn thing
    """
    ip = "localhost:{}".format(port)
    client = opc.Client(ip)

    while True:
        for temp in range(1667, 25001):
            pixels = flat_pixels(temp) * brightness
            client.put_pixels(pixels)
            time.sleep(sleep)

if __name__ == '__main__':
    main(sleep=0.0001, brightness=0.6)