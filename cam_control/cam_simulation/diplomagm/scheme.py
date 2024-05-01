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
"""This module contains functions that, 
based on the parameters of the field of interest to us 
and the list of panoramic systems that review the field of interest to us, 
implement visualization of fields of view and sharpness.
"""

import math
import numpy as np
import matplotlib.pyplot as plt

import basis
import camera as cmr
import field as fld
import panoramic_system as pano


def toMeters(value):
    """Conversion function from millimeters to meters.

    :param value: some value in millimeters
    :type value: float
    :return: the same value in meters
    :rtype: float
    """
    return value / 1000.0


def showFOV(field, list_of_panoramic_systems):
    """A function that builds a 2D-projection of the field of view
    based on the parameters of the field of interest to us and the list of panoramic systems 
    viewing the field of interest to us.

    :param field: parameters of the field we are interested in
    :type field: class Field
    :param list_of_panoramic_systems: list of panoramic systems that survey the field of interest to us
    :type list_of_panoramic_systems: class ListOfPanoramicSystems
    :return: field of view graph
    :rtype: figure
    """
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('axes', labelsize=16)

    fig = plt.figure(figsize=[16, 9])
    plt.axis("equal")

    field_length = field.getLength()
    field_width = field.getWidth()
    field_x = field.getCoordinatesX()
    field_y = field.getCoordinatesY()
    field_grandstand_width = field.getGrandstandWidth()
    field_a_coordinates, field_b_coordinates, field_c_coordinates, field_d_coordinates = field.getABCDCoordinates(
    )

    max_panoramic_system_x = 0.0
    max_panoramic_system_y = 0.0
    min_panoramic_system_x = 0.0
    min_panoramic_system_y = 0.0

    for panoramic_system in list_of_panoramic_systems.getListOfPanoramicSystems(
    ):
        panoramic_system_x, panoramic_system_y, panoramic_system_z = panoramic_system.getCoordinates(
        )
        if (panoramic_system_x > max_panoramic_system_x):
            max_panoramic_system_x = panoramic_system_x
        if (panoramic_system_x < min_panoramic_system_x):
            min_panoramic_system_x = panoramic_system_x
        if (panoramic_system_y > max_panoramic_system_y):
            max_panoramic_system_y = panoramic_system_y
        if (panoramic_system_y < min_panoramic_system_y):
            min_panoramic_system_y = panoramic_system_y

    min_x_lim = field_x - field_width / 2.0 - field_grandstand_width
    max_x_lim = field_x + field_width / 2.0 + field_grandstand_width
    min_y_lim = field_y - field_length / 2.0 - field_grandstand_width
    max_y_lim = field_y + field_length / 2.0 + field_grandstand_width

    if ((max_panoramic_system_x + field_grandstand_width) > max_x_lim):
        max_x_lim = max_panoramic_system_x + field_grandstand_width
    if ((min_panoramic_system_x - field_grandstand_width) < min_x_lim):
        min_x_lim = min_panoramic_system_x - field_grandstand_width
    if ((max_panoramic_system_y + field_grandstand_width) > max_y_lim):
        max_y_lim = max_panoramic_system_y + field_grandstand_width
    if ((min_panoramic_system_y - field_grandstand_width) < min_y_lim):
        min_y_lim = min_panoramic_system_y - field_grandstand_width

    x_field = np.array([
        field_a_coordinates.getCoordinatesX(),
        field_b_coordinates.getCoordinatesX(),
        field_c_coordinates.getCoordinatesX(),
        field_d_coordinates.getCoordinatesX(),
        field_a_coordinates.getCoordinatesX()
    ])

    y_field = np.array([
        field_a_coordinates.getCoordinatesY(),
        field_b_coordinates.getCoordinatesY(),
        field_c_coordinates.getCoordinatesY(),
        field_d_coordinates.getCoordinatesY(),
        field_a_coordinates.getCoordinatesY()
    ])

    plt.xlim(left=min_x_lim * 2, right=max_x_lim * 2)
    plt.ylim(bottom=min_y_lim * 1.5, top=max_y_lim * 1.5)

    plt.plot(x_field, y_field, color="green")
    #circle = plt.Circle((0.0, 0.0), 0.15, color='green', fill = False)
    #plt.gca().add_artist(circle)

    for panoramic_system in list_of_panoramic_systems.getListOfPanoramicSystems(
    ):

        panoramic_system_FOV = panoramic_system.calculatePanoramicSystemFOV()
        print(panoramic_system_FOV)

        for fov in panoramic_system.getListOfCamerasFOV():
            fov_x = np.array([
                fov.getVertexA().getCoordinatesX(),
                fov.getVertexB().getCoordinatesX(),
                fov.getVertexC().getCoordinatesX(),
                fov.getVertexD().getCoordinatesX(),
                fov.getVertexA().getCoordinatesX()
            ])
            fov_y = np.array([
                fov.getVertexA().getCoordinatesY(),
                fov.getVertexB().getCoordinatesY(),
                fov.getVertexC().getCoordinatesY(),
                fov.getVertexD().getCoordinatesY(),
                fov.getVertexA().getCoordinatesY()
            ])

            plt.plot(fov_x, fov_y, color="blue")

        for camera_axis in panoramic_system.getListOfCamerasAxis():
            camera_axis_x = np.array([
                camera_axis[0].getCoordinatesX(),
                camera_axis[1].getCoordinatesX()
            ])
            camera_axis_y = np.array([
                camera_axis[0].getCoordinatesY(),
                camera_axis[1].getCoordinatesY()
            ])

            plt.plot(camera_axis_x, camera_axis_y, linestyle='--', color="blue")

    plt.xlabel(xlabel='x, m', loc='right', fontsize=20)
    plt.ylabel(ylabel='y, m', loc='top', rotation=0, fontsize=20)

    plt.grid()
    plt.savefig('figures/FOV.png')
    plt.savefig('figures/FOV.eps')
    plt.show()

    return fig


def showFOS(field, list_of_panoramic_systems):
    """A function that builds a 2D-projection of the field of scharpness
    based on the parameters of the field of interest to us and the list of panoramic systems 
    viewing the field of interest to us.

    :param field: parameters of the field we are interested in
    :type field: class Field
    :param list_of_panoramic_systems: list of panoramic systems that survey the field of interest to us
    :type list_of_panoramic_systems: class ListOfPanoramicSystems
    :return: field of scharpness graph
    :rtype: figure
    """
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('axes', labelsize=16)

    fig = plt.figure(figsize=[16, 9])
    plt.axis("equal")

    field_length = field.getLength()
    field_width = field.getWidth()
    field_x = field.getCoordinatesX()
    field_y = field.getCoordinatesY()
    field_grandstand_width = field.getGrandstandWidth()
    field_a_coordinates, field_b_coordinates, field_c_coordinates, field_d_coordinates = field.getABCDCoordinates(
    )

    max_panoramic_system_x = 0.0
    max_panoramic_system_y = 0.0
    min_panoramic_system_x = 0.0
    min_panoramic_system_y = 0.0

    for panoramic_system in list_of_panoramic_systems.getListOfPanoramicSystems(
    ):
        panoramic_system_x, panoramic_system_y, panoramic_system_z = panoramic_system.getCoordinates(
        )
        if (panoramic_system_x > max_panoramic_system_x):
            max_panoramic_system_x = panoramic_system_x
        if (panoramic_system_x < min_panoramic_system_x):
            min_panoramic_system_x = panoramic_system_x
        if (panoramic_system_y > max_panoramic_system_y):
            max_panoramic_system_y = panoramic_system_y
        if (panoramic_system_y < min_panoramic_system_y):
            min_panoramic_system_y = panoramic_system_y

    min_x_lim = field_x - field_width / 2.0 - field_grandstand_width
    max_x_lim = field_x + field_width / 2.0 + field_grandstand_width
    min_y_lim = field_y - field_length / 2.0 - field_grandstand_width
    max_y_lim = field_y + field_length / 2.0 + field_grandstand_width

    if ((max_panoramic_system_x + field_grandstand_width) > max_x_lim):
        max_x_lim = max_panoramic_system_x + field_grandstand_width
    if ((min_panoramic_system_x - field_grandstand_width) < min_x_lim):
        min_x_lim = min_panoramic_system_x - field_grandstand_width
    if ((max_panoramic_system_y + field_grandstand_width) > max_y_lim):
        max_y_lim = max_panoramic_system_y + field_grandstand_width
    if ((min_panoramic_system_y - field_grandstand_width) < min_y_lim):
        min_y_lim = min_panoramic_system_y - field_grandstand_width

    x_field = np.array([
        field_a_coordinates.getCoordinatesX(),
        field_b_coordinates.getCoordinatesX(),
        field_c_coordinates.getCoordinatesX(),
        field_d_coordinates.getCoordinatesX(),
        field_a_coordinates.getCoordinatesX()
    ])

    y_field = np.array([
        field_a_coordinates.getCoordinatesY(),
        field_b_coordinates.getCoordinatesY(),
        field_c_coordinates.getCoordinatesY(),
        field_d_coordinates.getCoordinatesY(),
        field_a_coordinates.getCoordinatesY()
    ])

    plt.xlim(left=min_x_lim * 2, right=max_x_lim * 2)
    plt.ylim(bottom=min_y_lim * 1.5, top=max_y_lim * 1.5)

    plt.plot(x_field, y_field, color="green")

    #circle = plt.Circle((0.0, 0.0), 0.15, color='green', fill = False)
    #plt.gca().add_artist(circle)

    for panoramic_system in list_of_panoramic_systems.getListOfPanoramicSystems(
    ):

        panoramic_system.calculatePanoramicSystemFOS()

        for fos in panoramic_system.getListOfCamerasFOS():
            list_fos_x = []
            list_fos_y = []

            for point in fos:
                list_fos_x.append(point[0])
                list_fos_y.append(point[1])

            if (len(fos) > 2):
                list_fos_x.append(fos[0][0])
                list_fos_y.append(fos[0][1])

            fos_x = np.array(list_fos_x)
            fos_y = np.array(list_fos_y)

            plt.plot(fos_x, fos_y, color="gray")

        for camera_axis in panoramic_system.getListOfCamerasAxis():
            camera_axis_x = np.array([
                camera_axis[0].getCoordinatesX(),
                camera_axis[1].getCoordinatesX()
            ])
            camera_axis_y = np.array([
                camera_axis[0].getCoordinatesY(),
                camera_axis[1].getCoordinatesY()
            ])

            plt.plot(camera_axis_x, camera_axis_y, linestyle='--', color="gray")

    plt.xlabel(xlabel='x, m', loc='right', fontsize=20)
    plt.ylabel(ylabel='y, m', loc='top', rotation=0, fontsize=20)

    plt.grid()
    plt.savefig('figures/FOS.png')
    plt.savefig('figures/FOS.eps')
    plt.show()

    return fig
