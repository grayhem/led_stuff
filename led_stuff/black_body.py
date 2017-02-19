"""
we want to simulate the black body radiation color progression in RGB so we can use it in
RGBLED applications.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import skimage.color as color


def spline_approximation(temp):
    """
    given a temperature in kelvins, approximate the black body color using the 3-spline
    approach. color is returned as xy chromaticity values.
    see "Design of Advanced Color Temperature Control System for HDTV Applications"
    """

    if temp < 1667 or temp > 25000:
        raise ValueError("temperature out of range (1667-25000)")
    t = np.array([
        (1e9 / temp **3),
        (1e6 / temp ** 2),
        (1e3 / temp),
        1])
    exponents = np.arange(4)[::-1]
    if temp <= 2222:
        x_terms = np.array([
            -0.2661239,
            -0.2343580,
            0.8776956,
            0.179910])
        y_terms = np.array([
            -1.1063814,
            -1.3481102,
            2.18555832,
            -0.20219683])
    elif temp <= 4000:
        x_terms = np.array([
            -0.2661239,
            -0.2343580,
            0.8776956,
            0.179910])
        y_terms = np.array([
            -0.9549476,
            -1.37418593,
            2.09137015,
            -0.16748867])
    else:
        # up to 25000k
        x_terms = np.array([
            -3.0258469,
            2.1070379,
            0.2226347,
            0.240390])
        y_terms = np.array([
            3.0817580,
            -5.87338670,
            3.75112997,
            -0.3700143])
    x = np.dot(x_terms, t)
    y = np.dot(x**exponents, y_terms)
    return x, y

def xy_to_cie_xyz(x, y):
    """
    how do we convert chromaticity to the xyz space? wikipedia is awful.
    """
    return x, y, 1 - x - y

def temp_demo(temp, shape=(400, 400)):
    """
    plot a uniform image of a black body temperature mapped to rgb
    """
    xy = spline_approximation(temp)
    xyz_triple = np.asarray(xy_to_cie_xyz(*xy))
    xyz_image = np.ones((shape[0], shape[1], 3)) * xyz_triple.reshape(1, 1, 3)
    rgb = xyz_to_rgb(xyz_image)
    plt.figure()
    plt.imshow(rgb)
    plt.show()


def xyz_to_rgb(xyz_array):
    """
    convert xyz to rgb color space, and normalize all pixels and channels together.
    """
    rgb_array = color.xyz2rgb(xyz_array)
    return rgb_array / rgb_array.max()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        temp_demo(3000)
    elif len(sys.argv) == 2:
        temp_demo(int(sys.argv[1]))