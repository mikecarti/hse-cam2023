# MIT License

# Copyright (c) 2024 Matvey Gantsev

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module contains the camera class and its methods for storing, retrieving and changing camera parameters, 
as well as the image sensor and lens classes, that are part of the camera class, and their methods.
"""

import math
import numpy as np
from basis import Axis, Coordinates, Size
from rotation_matrix import getRotationMatrix


class Lens:
    """_summary_
    """

    def __init__(self, focal_length, f_number, focus_distance, body_diameter,
                 body_length):
        """_summary_

        :param focal_length: _description_
        :type focal_length: _type_
        :param f_number: _description_
        :type f_number: _type_
        :param focus_distance: _description_
        :type focus_distance: _type_
        :param body_diameter: _description_
        :type body_diameter: _type_
        :param body_length: _description_
        :type body_length: _type_
        """
        self.__focal_length = focal_length
        self.__f_number = f_number
        self.__focus_distance = focus_distance
        self.__diameter = body_diameter
        self.__length = body_length

    def getFocalLength(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__focal_length

    def getFNumber(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__f_number

    def getFocusDistance(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__focus_distance

    def getSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__diameter, self.__length

    def getDiameter(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__diameter

    def getLength(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__length


class ImageSensor:
    """_summary_
    """

    def __init__(self, width, height, pixel_size):
        """_summary_

        :param width: _description_
        :type width: _type_
        :param height: _description_
        :type height: _type_
        :param pixel_size: _description_
        :type pixel_size: _type_
        """
        self.__width = width
        self.__height = height
        self.__pixel_size = pixel_size

    def getSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__width, self.__height

    def getWidth(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__width

    def getHeight(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__heights

    def getPixelSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__pixel_size


class Camera:
    """_summary_
    """

    def __init__(self,
                 id,
                 focal_length,
                 f_number,
                 focus_distance,
                 diameter_of_lens,
                 lenght_of_lens,
                 width_of_image_sensor,
                 height_of_image_sensor,
                 pixel_size,
                 body_lenght,
                 body_width,
                 body_height,
                 x=0.0,
                 y=0.0,
                 z=0.0,
                 pitch=0.0,
                 yaw=0.0,
                 roll=0.0):
        """_summary_

        :param id: _description_
        :type id: _type_
        :param focal_length: _description_
        :type focal_length: _type_
        :param f_number: _description_
        :type f_number: _type_
        :param focus_distance: _description_
        :type focus_distance: _type_
        :param diameter_of_lens: _description_
        :type diameter_of_lens: _type_
        :param lenght_of_lens: _description_
        :type lenght_of_lens: _type_
        :param width_of_image_sensor: _description_
        :type width_of_image_sensor: _type_
        :param height_of_image_sensor: _description_
        :type height_of_image_sensor: _type_
        :param pixel_size: _description_
        :type pixel_size: _type_
        :param body_lenght: _description_
        :type body_lenght: _type_
        :param body_width: _description_
        :type body_width: _type_
        :param body_height: _description_
        :type body_height: _type_
        :param x: _description_, defaults to 0.0
        :type x: float, optional
        :param y: _description_, defaults to 0.0
        :type y: float, optional
        :param z: _description_, defaults to 0.0
        :type z: float, optional
        :param pitch: _description_, defaults to 0.0
        :type pitch: float, optional
        :param yaw: _description_, defaults to 0.0
        :type yaw: float, optional
        :param roll: _description_, defaults to 0.0
        :type roll: float, optional
        """
        self.__id = id
        self.__size = Size(body_lenght, body_width, body_height)
        self.__coordinates = Coordinates(x, y, z)
        self.__axis = Axis(pitch, yaw, roll)
        self.__rotationMatrix = getRotationMatrix(pitch, yaw, roll)
        self.__vector_x = np.dot(np.array([1, 0, 0]), self.__rotationMatrix)
        self.__vector_y = np.dot(np.array([0, 1, 0]), self.__rotationMatrix)
        self.__vector_z = np.dot(np.array([0, 0, 1]), self.__rotationMatrix)
        self.__diameter_of_lens = diameter_of_lens
        self.__lenght_of_lens = lenght_of_lens
        self.__f_number = f_number
        self.__focus_distance = focus_distance
        self.__height_of_image_sensor = height_of_image_sensor
        self.__lenght_of_lens = lenght_of_lens
        self.__width_of_image_sensor = width_of_image_sensor
        self.__pixel_size = pixel_size

        self._initialize_lens(focal_length)

    def _initialize_lens(self, focal_length):
        self.__lens = Lens(focal_length, self.__f_number, self.__focus_distance,
                           self.__diameter_of_lens, self.__lenght_of_lens)
        self.__imageSensor = ImageSensor(self.__width_of_image_sensor,
                                         self.__height_of_image_sensor, self.__pixel_size)
        self.__width_angle_of_view = 2 * math.atan(
            self.__width_of_image_sensor / 2 / focal_length) * 180 / math.pi
        self.__height_angle_of_view = 2 * math.atan(
            self.__height_of_image_sensor / 2 / focal_length) * 180 / math.pi
        self.__hyperfocal_distance = focal_length ** 2 / self.__f_number / (
                math.sqrt(2) * self.__pixel_size / 1000)

    def getID(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__id

    def getRotationMatrix(self):
        """_summary_
        """
        return self.__rotationMatrix

    def getBasicPyramidOfFOV(self):
        """_summary_
        """
        return self.__basicPyramidOfFOV

    def getHyperfocalDistance(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__hyperfocal_distance

    def getFocusDistance(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__lens.getFocusDistance()

    def getAnglesOfView(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__width_angle_of_view, self.__height_angle_of_view

    def getWidthAngleOfView(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__width_angle_of_view

    def getHeightAngleOfView(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__height_angle_of_view

    def getSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__size.getSize()

    def getLength(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__size.getLength()

    def getWidth(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__size.getWidth()

    def getHeight(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__size.getHeight()

    def getAxis(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__axis.getAxis()

    def getPitch(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__axis.getPitch()

    def getYaw(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__axis.getYaw()

    def getRoll(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__axis.getRoll()

    def getLensFocalLength(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__lens.getFocalLength()

    def setLensFocalLength(self, focal_length: float):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        self.__lens.__focal_length = focal_length
        self._initialize_lens(focal_length)

    def getLensSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__lens.getSize()

    def getLensDiameter(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__lens.getDiameter()

    def getLensLength(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__lens.getLength()


    def getImageSensorSize(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__imageSensor.getSize()

    def getCoordinates(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__coordinates.getCoordinates()

    def getCoordinatesX(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__coordinates.getCoordinatesX()

    def getCoordinatesY(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__coordinates.getCoordinatesY()

    def getCoordinatesZ(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.__coordinates.getCoordinatesZ()

    def printParameters(self):
        """_summary_
        """
        id = self.getID()
        lens_focal_lenght = self.getLensFocalLength()
        lens_diameter, lens_lenght = self.getLensSize()
        camera_lenght, camera_width, camera_height = self.getSize()
        image_sensor_width, image_sensor_height = self.getImageSensorSize()
        camera_x, camera_y, camera_z = self.getCoordinates()
        camera_pitch, camera_yaw, camera_roll = self.getAxis()
        width_angle_of_view, height_angle_of_view = self.getAnglesOfView()

        print("Camera №", id, ":")
        print(" Camera size:")
        print("     Lenght: ", f"{camera_lenght:.1f}", "mm")
        print("     Width: ", f"{camera_width:.1f}", "mm")
        print("     Height: ", f"{camera_height:.1f}", "mm")

        print(" Lens parameters:")
        print("     Lens focal lenght: ", f"{lens_focal_lenght:.1f}", "mm")
        print("     Lens diameter: ", f"{lens_diameter:.1f}", "mm")
        print("     Lens lenght: ", f"{lens_lenght:.1f}", "mm")

        print(" Image sensor size:")
        print("     Width: ", f"{image_sensor_width}", "mm")
        print("     Height: ", f"{image_sensor_height}", "mm")

        print(" Camera coordinates:")
        print("     x: ", f"{camera_x:.1f}", "mm")
        print("     y: ", f"{camera_y:.1f}", "mm")
        print("     z: ", f"{camera_z:.1f}", "mm")

        print(" Camera axis:")
        print("     pitch: ", f"{camera_pitch:.1f}", "degrees")
        print("     yaw: ", f"{camera_yaw:.1f}", "degrees")
        print("     roll: ", f"{camera_roll:.1f}", "degrees")

        print(" Width angle of view: ", f"{width_angle_of_view:.1f}", "degrees")
        print(" Height angle of view: ", f"{height_angle_of_view:.1f}",
              "degrees")

        print()
