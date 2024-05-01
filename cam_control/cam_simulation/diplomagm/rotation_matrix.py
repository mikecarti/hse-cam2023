"""This module contains functions for calculating rotation matrices around the x, y, z axes 
and a matrix that is a superposition of these rotation matrices around these three axes.
"""
import math
import numpy as np


def getYawRotationMatrix(yaw):
    """Calculate and return rotation matrix around the z axis.

    :param yaw: angle of rotation around the z axis
    :type yaw: float
    :return: rotation matrix around the z axis
    :rtype: numpy.array
    """
    return np.array(
        [[math.cos(math.radians(yaw)), -math.sin(math.radians(yaw)), 0],
         [math.sin(math.radians(yaw)),
          math.cos(math.radians(yaw)), 0], [0, 0, 1]])


def getPitchRotationMatrix(pitch):
    """Calculate and return rotation matrix around the y axis.

    :param yaw: angle of rotation around the y axis
    :type yaw: float
    :return: rotation matrix around the y axis
    :rtype: numpy.array
    """
    return np.array(
        [[math.cos(math.radians(pitch)), 0,
          math.sin(math.radians(pitch))], [0, 1, 0],
         [-math.sin(math.radians(pitch)), 0,
          math.cos(math.radians(pitch))]])


def getRollRotationMatrix(roll):
    """Calculate and return rotation matrix around the x axis.

    :param yaw: angle of rotation around the x axis
    :type yaw: float
    :return: rotation matrix around the x axis
    :rtype: numpy.array
    """
    return np.array(
        [[1, 0, 0],
         [0, math.cos(math.radians(roll)), -math.sin(math.radians(roll))],
         [0, math.sin(math.radians(roll)),
          math.cos(math.radians(roll))]])


def getRotationMatrix(pitch, yaw, roll):
    """Calculate and return superposition of three rotation matrices about the x, y, z axes.

    :param pitch: angle of rotation around the y axis
    :type pitch: numpy.array
    :param yaw: angle of rotation around the z axis
    :type yaw: numpy.array
    :param roll: angle of rotation around the x axis
    :type roll: numpy.array
    :return: final rotation matrix around the x, y, z axes
    :rtype: numpy.array
    """

    yawRotationMatrix = getYawRotationMatrix(yaw)
    pitchRotationMatrix = getPitchRotationMatrix(pitch)
    rollRotationMatrix = getRollRotationMatrix(roll)

    return np.dot(np.dot(yawRotationMatrix, pitchRotationMatrix),
                  rollRotationMatrix)
