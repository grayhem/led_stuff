"""
let's try using slerp to interpolate between random colors on a sphere in RGB color space.
next will probably be doing something like that in another color space.
so we could rotate our unit vector about the origin and translate/ scale manually.
or we could compose an se3 affine transformation matrix with correct translation and
scale parameters and do it all in one shot.

"""

import sys
import time

import numpy as np

from led_stuff import transformations

SEED = None

# let's not ever exceed this energy level (fraction of 255) on any channel
MAX_BRIGHTNESS = 0.75

# epsilon for testing whether a number is close to zero
_EPS = numpy.finfo(float).eps * 4.0



# start with a random vector representing our color, in R3 -1, 1
# color = np.random.uniform(low=-1, high=1, size=3)
# note we can also make some kind of fancy shape on the matrix and rotate the whole thing
# then we would just flatten the first two axes (color is on the third) and dot with the
# transformation matrix, then pop back to original shape.

# generate an identity quaternion to start with
# start_quaternion = np.array(1.0, 0.0, 0.0, 0.0)

# generate a random quaternion to which to slerp


# slerp at each and every interval
# what happens if we change the interval or the angular distance traveled per interval, as
# time goes on?


# take our slerped quaternion and make a rotation matrix

# compose into a transformation matrix with scale and translation

# perform the transformation



# make a generator that yields slerped quaternions, given the two end quaternions. it should
# yield the first end quaternion unmolested on the first iteration, and then the last iteration
# should yield the last quaternion before the end quaternion.
# we shouldn't give it a set number of steps; rather, we should specify a certain distance
# for each step. unless we want it to speed up and slow down at random, depending on how
# far apart the two quaternions are. which we might.
# also we will only generate smooth trajectories between two given endpoints; every time the
# generator is restarted it will introduce a discontinuity. something something keep a buffer
# of the last however many end quaternions and use a spline...
# we could also just let the generator run forever and on every iteration it picks a new
# endpoint that's just slightly different from the original and rotates like 5% of the way there.
# we could even pick those shifting goalpost quaternions by doing the same thing-- take an
# original quaternion, pick a random new one to rotate towards and interpolate along the path.


# what if we don't want to take the shortest path?

# while True
#     end_quaternion = transformations.random_quaternion()
#     for this_quaternion in slerp(start_quaternion, end_quaternion, steps):
#         # do the stuff
#         time.sleep(delay)


def slerp(start, end, steps):
    """
    slerp from start to end in a fixed number of steps.
    """
    for fraction in np.linspace(0, 1, num=steps, endpoint=False):
        yield transformations.quaternion_slerp(start, end, fraction)

def uniform_slerp(start, end, degrees):
    """
    slerp from start to end at a constant angular velocity (deg per iteration).
    it's only approximately uniform. we round up the number of steps in the path so the
    steps will be slightly smaller than is strictly accurate.
    """

    # first get the angle of the arc between the two quaternions
    angle = angle_between_quaternions(start, end)

    # divide it up to get our fractions
    steps = int(np.ceil(angle / degrees))

    yield from slerp(start, end, steps)


def goalpost_slerp(start, end, fraction):
    """
    slerp from start to end, but random walk the end point.
    we random walk the end point by composing it with a random quaternion representing a
    rotation which is not necessarily that small. it might be tricky to find a combination
    of parameters (slerp fraction and how-far-to-move-goalpost) that explores the color space
    in an aesthetically pleasing time scale.
    """
    pass

def angle_between_quaternions(a, b):
    """
    measure the angle of the shortest path between two quaternions
    """
    a = transformations.unit_vector(a[:4])
    b = transformations.unit_vector(b[:4])
    dot = np.dot(a, b)
    if abs(abs(dot) - 1.0) < _EPS:
        return 0
    if dot < 0.0:
        # invert rotation
        dot = -dot
        np.negative(q1, q1)
    angle = np.degrees(np.arccos(d))
    return angle


if __name__ == '__main__':
    # seed the random number generator?
    if SEED is not None
        np.random.seed(SEED)

    if BRIGHTNESS > MAX_BRIGHTNESS:
        print("capping brightness at {} (mind your power supply)".format(MAX_BRIGHTNESS))
        BRIGHTNESS = MAX_BRIGHTNESS

