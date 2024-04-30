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
"""This module contains classes and their methods for creating panoramic systems, 
obtaining and changing their parameters, as well as for calculating their 
fields of view and sharpness.
"""

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from basis import Coordinates, Axis, Size, Tetragon
from rotation_matrix import getRotationMatrix


def toMeters(value):
    """Conversion function from millimeters to meters.

    :param value: some value in millimeters
    :type value: float
    :return: the same value in meters
    :rtype: float
    """
    return value / 1000.0


class ListOfPanoramicSystems:
    """The class contains a list of all panoramic systems 
    that we use to review the field of interest to us, 
    as well as the parameters of all these panoramic systems.
    """

    def __init__(self):
        """Class ListOfPanoramicSystems constructor.
        """
        self.__number_of_panoramic_systems = 0
        self.__list_of_panoramic_systems = []

    def clear(self):
        """Remove all panoramic systems from this list.
        """
        self.__number_of_panoramic_systems = 0
        self.__list_of_panoramic_systems.clear()

    def getNumberOfPanoramicSystems(self):
        """Get number of panoramic systems in list of panoramic systems.

        :return: number of panoramic systems in list of panoramic systems
        :rtype: int
        """
        return self.__number_of_panoramic_systems

    def addPanoramicSystem(self, panoramic_system):
        """Add panoramic system to the end of list of panoramic stystems.

        :param panoramic_system: new panoramic system that we want to add to the end of the list of panoramic systems
        :type panoramic_system: class PanoramicSystem
        """
        self.__number_of_panoramic_systems = self.__number_of_panoramic_systems + 1
        self.__list_of_panoramic_systems.append(panoramic_system)

    def removePanoramicSystem(self, panoramic_system_id):
        """Remove a panoramic system from the list of panoramic systems by its id.

        :param panoramic_system_id: id number of the panoramic system we want to remove
        :type panoramic_system_id: int
        """
        self.__number_of_panoramic_systems = self.__number_of_panoramic_systems - 1
        self.__list_of_panoramic_systems.pop(panoramic_system_id)

    def getListOfPanoramicSystems(self):
        """Get a list of panoramic systems.

        :return: list of panoramic systems
        :rtype: list
        """
        return self.__list_of_panoramic_systems

    def printParameters(self):
        """Print the parameters of all panoramic systems from the list.
        """
        list_of_panoramic_systems = self.getListOfPanoramicSystems()

        for panoramic_system in list_of_panoramic_systems:
            panoramic_system.printParameters()


class PanoramicSystem:
    """A panoramic system class that allows you to store all the parameters of a panoramic system, 
    receive and change these parameters, as well as calculate the view and sharpness fields of panoramic systems.
    """

    def __init__(self,
                 id,
                 body_lenght=0.0,
                 body_width=0.0,
                 body_height=0.0,
                 x=0.0,
                 y=0.0,
                 z=0.0,
                 pitch=0.0,
                 yaw=0.0,
                 roll=0.0):
        """A constructor for the panoramic camera class that, 
        based on the incoming parameters, builds a panoramic system 
        with the specified parameters.

        :param id: id number of panoramic system in list of panoramic systems
        :type id: int
        :param body_lenght: length of panoramic systems body, defaults to 0.0
        :type body_lenght: float, optional
        :param body_width: width of panoramic systems body, defaults to 0.0
        :type body_width: float, optional
        :param body_height: height of panoramic systems body, defaults to 0.0
        :type body_height: float, optional
        :param x: coordinate x of the center of the panoramic system body in space, defaults to 0.0
        :type x: float, optional
        :param y: coordinate y of the center of the panoramic system body in space, defaults to 0.0
        :type y: float, optional
        :param z: coordinate z of the center of the panoramic system body in space, defaults to 0.0
        :type z: float, optional
        :param pitch: panoramic system pitch angle, defaults to 0.0
        :type pitch: float, optional
        :param yaw: panoramic system yaw angle, defaults to 0.0
        :type yaw: float, optional
        :param roll: panoramic system roll angle, defaults to 0.0
        :type roll: float, optional
        """
        self.__id = id
        self.__number_of_cameras = 0
        self.__size = Size(body_lenght, body_width, body_height)
        self.__coordinates = Coordinates(x, y, z)
        self.__axis = Axis(pitch, yaw, roll)
        self.__rotationMatrix = getRotationMatrix(pitch, yaw, roll)
        self.__vector_x = np.dot(np.array([1, 0, 0]), self.__rotationMatrix)
        self.__vector_y = np.dot(np.array([0, 1, 0]), self.__rotationMatrix)
        self.__vector_z = np.dot(np.array([0, 0, 1]), self.__rotationMatrix)
        self.__list_of_cameras_displacement_vectors = []
        self.__list_of_cameras_rotation_matrices = []
        self.__list_of_cameras = []
        self.__list_of_cameras_fov = []
        self.__list_of_cameras_fos = []
        self.__list_of_cameras_axis = []

    def changeProperties(self,
                         id,
                         lenght=None,
                         width=None,
                         height=None,
                         x=None,
                         y=None,
                         z=None,
                         pitch=None,
                         yaw=None,
                         roll=None):
        """Changing the parameters of an existing system based on incoming parameters.

        :param id: id number of panoramic system in list of panoramic systems
        :type id: int
        :param body_lenght: length of panoramic systems body, defaults to 0.0
        :type body_lenght: float, optional
        :param body_width: width of panoramic systems body, defaults to 0.0
        :type body_width: float, optional
        :param body_height: height of panoramic systems body, defaults to 0.0
        :type body_height: float, optional
        :param x: coordinate x of the center of the panoramic system body in space, defaults to 0.0
        :type x: float, optional
        :param y: coordinate y of the center of the panoramic system body in space, defaults to 0.0
        :type y: float, optional
        :param z: coordinate z of the center of the panoramic system body in space, defaults to 0.0
        :type z: float, optional
        :param pitch: panoramic system pitch angle, defaults to 0.0
        :type pitch: float, optional
        :param yaw: panoramic system yaw angle, defaults to 0.0
        :type yaw: float, optional
        :param roll: panoramic system roll angle, defaults to 0.0
        :type roll: float, optional
        """
        self.__id = id
        if None not in (lenght, width, height):
            self.__size = Size(lenght, width, height)
        if None not in (x,y,z):
            self.__coordinates = Coordinates(x, y, z)
        if roll is None:
            print("Warning, roll is None")
        if None not in (pitch, yaw, roll):
            self.__axis = Axis(pitch, yaw, roll)
            self.__rotationMatrix = getRotationMatrix(pitch, yaw, roll)
            self.__vector_x = np.dot(np.array([1, 0, 0]), self.__rotationMatrix)
            self.__vector_y = np.dot(np.array([0, 1, 0]), self.__rotationMatrix)
            self.__vector_z = np.dot(np.array([0, 0, 1]), self.__rotationMatrix)
        # self.__list_of_cameras_displacement_vectors = []
        # self.__list_of_cameras_rotation_matrices = []
        # self.__list_of_cameras = []
        # self.__list_of_cameras_fov = []
        # self.__list_of_cameras_fos = []
        # self.__list_of_cameras_axis = []

    def changePropertiesFromData(self, data):
        """Changing the parameters of an existing system based on data received in the JSON-format.

        :param data: data in the JSON-format
        :type data: dictionary
        """
        self.__id = data['id']
        self.__size = Size(data['size']['length'], data['size']['width'],
                           data['size']['height'])
        self.__coordinates = Coordinates(data['coordinates']['x'],
                                         data['coordinates']['y'],
                                         data['coordinates']['z'])
        self.__axis = Axis(data['axis']['pitch'], data['axis']['yaw'],
                           data['axis']['roll'])
        self.__rotationMatrix = getRotationMatrix(data['axis']['pitch'], data['axis']['yaw'], data['axis']['roll'])
        self.__vector_x = np.dot(np.array([1, 0, 0]), self.__rotationMatrix)
        self.__vector_y = np.dot(np.array([0, 1, 0]), self.__rotationMatrix)
        self.__vector_z = np.dot(np.array([0, 0, 1]), self.__rotationMatrix)
        self.__list_of_cameras_displacement_vectors = []
        self.__list_of_cameras_rotation_matrices = []
        self.__list_of_cameras = []
        self.__list_of_cameras_fov = []
        self.__list_of_cameras_fos = []
        self.__list_of_cameras_axis = []

    def getID(self):
        """Get id number of the panoramic system in the list of panoramic systems.

        :return: id number of the panoramic system in the list of panoramic systems
        :rtype: int
        """
        return self.__id

    def getRotationMatrix(self):
        """Get a rotation matrix of the panoramic system 
        calculated according to the angles defining the orientation 
        of the panoramic system in space.

        :return: rotation matrix of the panoramic system
        :rtype: numpy.array
        """
        return self.__rotationMatrix

    def getNumberOfCameras(self):
        """Get the number of cameras that form the panoramic system.

        :return: number of cameras
        :rtype: int
        """
        return self.__number_of_cameras

    def addCamera(self, camera):
        """Add a new camera to the end of the list of cameras 
        that form this panoramic system.

        :param camera: new camera in panoramic system
        :type camera: class Camera
        """
        x, y, z = self.getCoordinates()
        camera_x, camera_y, camera_z = camera.getCoordinates()
        self.__number_of_cameras = self.__number_of_cameras + 1
        self.__list_of_cameras.append(camera)
        self.__list_of_cameras_displacement_vectors.append(
            np.array([x, y, z]) +
            np.dot(np.array([camera_x, camera_y, camera_z]),
                   self.__rotationMatrix))
        self.__list_of_cameras_rotation_matrices.append(
            np.dot(self.__rotationMatrix, camera.getRotationMatrix()))

    def removeCamera(self, camera_id):
        """Remove the camera from the list of cameras 
        that form this panoramic system by its id number.

        :param camera_id: id number of the camera we want to remove
        :type camera_id: int
        """
        self.__number_of_cameras = self.__number_of_cameras - 1
        self.__list_of_cameras.pop(camera_id)

    def getSize(self):
        """Get size of the panoramic system body.

        :return: size of the panoramic system body
        :rtype: class Size
        """
        return self.__size.getSize()

    def getLength(self):
        """Get length of the panoramic system body.

        :return: length of the panoramic system body
        :rtype: float
        """
        return self.__size.getLength()

    def getWidth(self):
        """Get width of the panoramic system body.

        :return: width of the panoramic system body
        :rtype: float
        """
        return self.__size.getWidth()

    def getHeight(self):
        """Get height of the panoramic system body.

        :return: height of the panoramic system body
        :rtype: float
        """
        return self.__size.getHeight()

    def getAxis(self):
        """Get angles that specify the orientation of the panoramic system in space.

        :return: angles of the panoramic system
        :rtype: class Axis
        """
        return self.__axis.getAxis()

    def getPitch(self):
        """Get pitch angle of the panoramic system.

        :return: pitch angle of the panoramic system
        :rtype: float
        """
        return self.__axis.getAxisPitch()

    def getYaw(self):
        """Get yaw angle of the panoramic system.

        :return: yaw angle of the panoramic system
        :rtype: float
        """
        return self.__axis.getAxisYaw()

    def getRoll(self):
        """Get roll angle of the panoramic system.

        :return: roll angle of the panoramic system
        :rtype: float
        """
        return self.__axis.getAxiisRoll()

    def getCoordinates(self):
        """Get the coordinates of the center of the panoramic system body in space.

        :return: coordinates of the center of the panoramic system body
        :rtype: class Coordinates
        """
        return self.__coordinates.getCoordinates()

    def getCoordinatesX(self):
        """Get the coordinate x of the center of the panoramic system body in space.

        :return: coordinate x of the center of the panoramic system body
        :rtype: float
        """
        return self.__coordinates.getCoordinatesX()

    def getCoordinatesY(self):
        """Get the coordinate y of the center of the panoramic system body in space.

        :return: coordinate y of the center of the panoramic system body
        :rtype: float
        """
        return self.__coordinates.getCoordinatesY()

    def getCoordinatesZ(self):
        """Get the coordinate z of the center of the panoramic system body in space.

        :return: coordinate z of the center of the panoramic system body
        :rtype: float
        """
        return self.__coordinates.getCoordinatesZ()

    def getListOfCameras(self):
        """Get list of cameras that form the panoramic system with their parameters.

        :return: list of cameras
        :rtype: list
        """
        return self.__list_of_cameras

    def getListOfCamerasFOV(self):
        """Get list of FOV of cameras that form the panoramic system. 
        Camera FOV are specified by arrays containing four vectors with point coordinates.

        :return: list of cameras FOV
        :rtype: list
        """
        return self.__list_of_cameras_fov

    def getListOfCamerasFOS(self):
        """Get list of FOS of cameras that form the panoramic system. 
        Camera FOS are specified by arrays containing some vectors with point coordinates.

        :return: list of cameras FOS
        :rtype: list
        """
        return self.__list_of_cameras_fos

    def getListOfCamerasAxis(self):
        """Get list of main optical axis of cameras that form the panoramic system. 
        Camera axis are specified by arrays containing two vectors with point coordinates.

        :return: list of cameras main optical axis
        :rtype: list
        """
        return self.__list_of_cameras_axis

    def printParameters(self):
        """Print panoramic system parameters.
        """
        panoramic_system_id = self.getID()
        panoramic_system = self.getListOfCameras()
        print("Panoramic system №", panoramic_system_id, ":")

        for camera in panoramic_system:
            camera.printParameters()
        print()

    def calculatePanoramicSystemFOV(self):
        """Calculate FOV for each camera in panoramic system and return list of cameras FOV for panoramic system. 

        :return: list of cameras FOV for panoramic system
        :rtype: list
        """

        list_of_cameras_FOV = []

        earth_circumference = 40000000
        self.__list_of_cameras_fov.clear()
        self.__list_of_cameras_axis.clear()

        A = 0
        B = 0
        C = 1
        D = 0

        vector_plane = np.array([A, B, C])

        panoramic_system_x, panoramic_system_y, panoramic_system_z = self.getCoordinates(
        )
        panoramic_system_coordinates = np.array(
            [panoramic_system_x, panoramic_system_y, panoramic_system_z])
        panoramic_system_pitch, panoramic_system_yaw, panoramic_system_roll = self.getAxis(
        )
        panoramic_system_rotation_matrix = self.getRotationMatrix()

        for camera in self.getListOfCameras():
            camera_z = toMeters(camera.getCoordinatesZ())
            camera_x = toMeters(camera.getCoordinatesX())
            camera_y = toMeters(camera.getCoordinatesY())
            camera_coordinates = np.array([camera_x, camera_y, camera_z])
            camera_rotation_matrix = camera.getRotationMatrix()
            camera_height_angle_of_view = camera.getHeightAngleOfView()
            camera_width_angle_of_view = camera.getWidthAngleOfView()

            vector_a = np.array([
                1.0,
                math.tan(math.radians(camera_width_angle_of_view / 2)),
                -math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_b = np.array([
                1.0,
                math.tan(math.radians(camera_width_angle_of_view / 2)),
                math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_c = np.array([
                1.0, -math.tan(math.radians(camera_width_angle_of_view / 2)),
                math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_d = np.array([
                1.0, -math.tan(math.radians(camera_width_angle_of_view / 2)),
                -math.tan(math.radians(camera_height_angle_of_view / 2))
            ])

            vector_p = np.array([1, 0, 0])

            vector_a = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_a)
            vector_b = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_b)
            vector_c = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_c)
            vector_d = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_d)
            vector_p = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_p)

            vector_t_0 = panoramic_system_coordinates + np.dot(
                panoramic_system_rotation_matrix, camera_coordinates)

            a_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_a))
            b_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_b))
            c_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_c))
            d_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_d))
            p_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_p))

            if (a_0 < 0):
                a_0 = earth_circumference

            if (b_0 < 0):
                b_0 = earth_circumference

            if (c_0 < 0):
                c_0 = earth_circumference

            if (d_0 < 0):
                d_0 = earth_circumference

            if (p_0 < 0):
                p_0 = earth_circumference

            fov_a = np.dot(a_0, vector_a) + vector_t_0
            fov_b = np.dot(b_0, vector_b) + vector_t_0
            fov_c = np.dot(c_0, vector_c) + vector_t_0
            fov_d = np.dot(d_0, vector_d) + vector_t_0
            main_axis = np.dot(p_0, vector_p) + vector_t_0

            camera_fov = Tetragon(fov_a[0], fov_a[1], fov_a[2], fov_b[0],
                                  fov_b[1], fov_b[2], fov_c[0], fov_c[1],
                                  fov_c[2], fov_d[0], fov_d[1], fov_d[2])

            self.__list_of_cameras_fov.append(camera_fov)

            camera_main_axis = np.array([
                Coordinates(vector_t_0[0], vector_t_0[1], vector_t_0[2]),
                Coordinates(main_axis[0], main_axis[1], main_axis[2])
            ])
            self.__list_of_cameras_axis.append(camera_main_axis)

            list_of_cameras_FOV.append([fov_a, fov_b, fov_c, fov_d])

        return list_of_cameras_FOV

    def calculatePanoramicSystemFOS(self):
        """Calculate FOS for each camera in panoramic system and return list of cameras FOV for panoramic system.

        :return: list of cameras FOS for panoramic system
        :rtype: list
        """
        earth_circumference = 40000000
        self.__list_of_cameras_fov.clear()
        self.__list_of_cameras_axis.clear()

        A = 0
        B = 0
        C = 1
        D = 0

        vector_plane = np.array([A, B, C])

        panoramic_system_x, panoramic_system_y, panoramic_system_z = self.getCoordinates(
        )
        panoramic_system_coordinates = np.array(
            [panoramic_system_x, panoramic_system_y, panoramic_system_z])
        panoramic_system_pitch, panoramic_system_yaw, panoramic_system_roll = self.getAxis(
        )
        panoramic_system_rotation_matrix = self.getRotationMatrix()

        for camera in self.getListOfCameras():
            hyperfocal_distance = toMeters(camera.getHyperfocalDistance())
            focus_distance = camera.getFocusDistance()

            fos_close = hyperfocal_distance**2 * focus_distance / (
                hyperfocal_distance + focus_distance * hyperfocal_distance)
            fos_far = hyperfocal_distance**2 * focus_distance / (
                hyperfocal_distance - focus_distance * hyperfocal_distance)

            camera_z = toMeters(camera.getCoordinatesZ())
            camera_x = toMeters(camera.getCoordinatesX())
            camera_y = toMeters(camera.getCoordinatesY())
            camera_coordinates = np.array([camera_x, camera_y, camera_z])
            camera_rotation_matrix = camera.getRotationMatrix()
            camera_height_angle_of_view = camera.getHeightAngleOfView()
            camera_width_angle_of_view = camera.getWidthAngleOfView()

            vector_a = np.array([
                1.0,
                math.tan(math.radians(camera_width_angle_of_view / 2)),
                -math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_b = np.array([
                1.0,
                math.tan(math.radians(camera_width_angle_of_view / 2)),
                math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_c = np.array([
                1.0, -math.tan(math.radians(camera_width_angle_of_view / 2)),
                math.tan(math.radians(camera_height_angle_of_view / 2))
            ])
            vector_d = np.array([
                1.0, -math.tan(math.radians(camera_width_angle_of_view / 2)),
                -math.tan(math.radians(camera_height_angle_of_view / 2))
            ])

            vector_p = np.array([1, 0, 0])

            vector_a = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_a)
            vector_b = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_b)
            vector_c = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_c)
            vector_d = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_d)
            vector_p = np.dot(
                np.dot(panoramic_system_rotation_matrix,
                       camera_rotation_matrix), vector_p)

            vector_t_0 = panoramic_system_coordinates + np.dot(
                panoramic_system_rotation_matrix, camera_coordinates)

            fov_a_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_a))
            fov_b_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_b))
            fov_c_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_c))
            fov_d_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_d))
            fov_p_0 = -(np.dot(vector_plane, vector_t_0) + D) / (np.dot(
                vector_plane, vector_p))

            if (fov_a_0 < 0):
                fov_a_0 = earth_circumference

            if (fov_b_0 < 0):
                fov_b_0 = earth_circumference

            if (fov_c_0 < 0):
                fov_c_0 = earth_circumference

            if (fov_d_0 < 0):
                fov_d_0 = earth_circumference

            if (fov_p_0 < 0):
                fov_p_0 = earth_circumference

            fov_a = np.dot(fov_a_0, vector_a) + vector_t_0
            fov_b = np.dot(fov_b_0, vector_b) + vector_t_0
            fov_c = np.dot(fov_c_0, vector_c) + vector_t_0
            fov_d = np.dot(fov_d_0, vector_d) + vector_t_0
            main_axis = np.dot(fov_p_0, vector_p) + vector_t_0

            camera_fov = Tetragon(fov_a[0], fov_a[1], fov_a[2], fov_b[0],
                                  fov_b[1], fov_b[2], fov_c[0], fov_c[1],
                                  fov_c[2], fov_d[0], fov_d[1], fov_d[2])

            vector_ab, point_ab, vector_bc, point_bc, vector_cd, point_cd, vector_da, point_da = camera_fov.getLines(
            )
            self.__list_of_cameras_fov.append(camera_fov)

            vector_p_lenght = math.sqrt(vector_p[0]**2 + vector_p[1]**2 +
                                        vector_p[2]**2)

            fos_close_0 = fos_close / vector_p_lenght
            fos_far_0 = fos_far / vector_p_lenght

            vector_plane_fos_close = vector_p
            vector_plane_fos_far = vector_p

            point_of_plane_fos_close = vector_t_0 + vector_plane_fos_close * fos_close_0
            point_of_plane_fos_far = vector_t_0 + vector_plane_fos_far * fos_far_0

            D_close = -(np.dot(vector_plane_fos_close,
                               point_of_plane_fos_close))
            D_far = -(np.dot(vector_plane_fos_far, point_of_plane_fos_far))

            ab_close_0 = -(np.dot(vector_plane_fos_close, point_ab) + D_close
                          ) / (np.dot(vector_plane_fos_close, vector_ab))
            bc_close_0 = -(np.dot(vector_plane_fos_close, point_bc) + D_close
                          ) / (np.dot(vector_plane_fos_close, vector_bc))
            cd_close_0 = -(np.dot(vector_plane_fos_close, point_cd) + D_close
                          ) / (np.dot(vector_plane_fos_close, vector_cd))
            da_close_0 = -(np.dot(vector_plane_fos_close, point_da) + D_close
                          ) / (np.dot(vector_plane_fos_close, vector_da))

            ab_far_0 = -(np.dot(vector_plane_fos_far, point_ab) + D_far) / (
                np.dot(vector_plane_fos_far, vector_ab))
            bc_far_0 = -(np.dot(vector_plane_fos_far, point_bc) + D_far) / (
                np.dot(vector_plane_fos_far, vector_bc))
            cd_far_0 = -(np.dot(vector_plane_fos_far, point_cd) + D_far) / (
                np.dot(vector_plane_fos_far, vector_cd))
            da_far_0 = -(np.dot(vector_plane_fos_far, point_da) + D_far) / (
                np.dot(vector_plane_fos_far, vector_da))

            fos_ab_close = None
            fos_bc_close = None
            fos_cd_close = None
            fos_da_close = None

            if (ab_close_0 > 0.0 and ab_close_0 < 1.0):
                fos_ab_close = ab_close_0 * vector_ab + point_ab

            if (bc_close_0 > 0.0 and bc_close_0 < 1.0):
                fos_bc_close = bc_close_0 * vector_bc + point_bc

            if (cd_close_0 > 0.0 and cd_close_0 < 1.0):
                fos_cd_close = cd_close_0 * vector_cd + point_cd

            if (da_close_0 > 0.0 and da_close_0 < 1.0):
                fos_da_close = da_close_0 * vector_da + point_da

            fos_ab_far = None
            fos_bc_far = None
            fos_cd_far = None
            fos_da_far = None

            if (ab_far_0 > 0.0 and ab_far_0 < 1.0):
                fos_ab_far = ab_far_0 * vector_ab + point_ab

            if (bc_far_0 > 0.0 and bc_far_0 < 1.0):
                fos_bc_far = bc_far_0 * vector_bc + point_bc

            if (cd_far_0 > 0.0 and cd_far_0 < 1.0):
                fos_cd_far = cd_far_0 * vector_cd + point_cd

            if (da_far_0 > 0.0 and da_far_0 < 1.0):
                fos_da_far = da_far_0 * vector_da + point_da

            camera_fos = []

            if ((np.dot(vector_plane_fos_close, fov_a) + D_close >= 0) and
                (np.dot(vector_plane_fos_far, fov_a) + D_far <= 0)):
                camera_fos.append(fov_a)
            elif (np.dot(vector_plane_fos_far, fov_a) + D_far > 0):
                if (fos_da_far is not None):
                    camera_fos.append(fos_da_far)
                if (fos_ab_far is not None):
                    camera_fos.append(fos_ab_far)
            elif (np.dot(vector_plane_fos_close, fov_a) + D_close < 0):
                if (fos_da_close is not None):
                    camera_fos.append(fos_da_close)
                if (fos_ab_close is not None):
                    camera_fos.append(fos_ab_close)
            else:
                pass

            if ((np.dot(vector_plane_fos_close, fov_b) + D_close >= 0) and
                (np.dot(vector_plane_fos_far, fov_b) + D_far <= 0)):
                camera_fos.append(fov_b)
            elif (np.dot(vector_plane_fos_far, fov_b) + D_far > 0):
                if (fos_ab_far is not None):
                    camera_fos.append(fos_ab_far)
                if (fos_bc_far is not None):
                    camera_fos.append(fos_bc_far)
            elif (np.dot(vector_plane_fos_close, fov_a) + D_close < 0):
                if (fos_ab_close is not None):
                    camera_fos.append(fos_ab_close)
                if (fos_bc_close is not None):
                    camera_fos.append(fos_bc_close)
            else:
                pass

            if ((np.dot(vector_plane_fos_close, fov_c) + D_close >= 0) and
                (np.dot(vector_plane_fos_far, fov_c) + D_far <= 0)):
                camera_fos.append(fov_c)
            elif (np.dot(vector_plane_fos_far, fov_c) + D_far > 0):
                if (fos_bc_far is not None):
                    camera_fos.append(fos_bc_far)
                if (fos_cd_far is not None):
                    camera_fos.append(fos_cd_far)
            elif (np.dot(vector_plane_fos_close, fov_c) + D_close < 0):
                if (fos_bc_close is not None):
                    camera_fos.append(fos_bc_close)
                if (fos_cd_close is not None):
                    camera_fos.append(fos_cd_close)
            else:
                pass

            if ((np.dot(vector_plane_fos_close, fov_d) + D_close >= 0) and
                (np.dot(vector_plane_fos_far, fov_d) + D_far <= 0)):
                camera_fos.append(fov_d)
            elif (np.dot(vector_plane_fos_far, fov_d) + D_far > 0):
                if (fos_cd_far is not None):
                    camera_fos.append(fos_cd_far)
                if (fos_da_far is not None):
                    camera_fos.append(fos_da_far)
            elif (np.dot(vector_plane_fos_close, fov_d) + D_close < 0):
                if (fos_cd_close is not None):
                    camera_fos.append(fos_cd_close)
                if (fos_da_close is not None):
                    camera_fos.append(fos_da_close)
            else:
                pass

            self.__list_of_cameras_fos.append(camera_fos)

            camera_main_axis = np.array([
                Coordinates(vector_t_0[0], vector_t_0[1], vector_t_0[2]),
                Coordinates(main_axis[0], main_axis[1], main_axis[2])
            ])
            self.__list_of_cameras_axis.append(camera_main_axis)

        return self.__list_of_cameras_fos

    def showPanoramicSystem(self):
        """View the body of the panoramic system up close to ensure 
        that the camera lenses don't block the view of other cameras in the panoramic system.
        """
        plt.rc('xtick', labelsize=14)
        plt.rc('ytick', labelsize=14)
        plt.rc('axes', labelsize=14)

        plt.figure(figsize=[16, 9])
        plt.axis("equal")
        panoramic_system = self.getListOfCameras()

        # show cameras body
        for camera in panoramic_system:
            camera_x = camera.getCoordinatesX()
            camera_y = camera.getCoordinatesY()
            camera_length = camera.getLength()
            camera_width = camera.getWidth()
            camera_yaw = camera.getYaw()

            camera_a_x = camera_x \
                - math.cos(math.radians(camera_yaw)) * (camera_length / 2.0) \
                - math.sin(math.radians(camera_yaw)) * (camera_width / 2.0)
            camera_a_y = camera_y \
                - math.sin(math.radians(camera_yaw)) * (camera_length / 2.0) \
                + math.cos(math.radians(camera_yaw)) * (camera_width / 2.0)

            camera_b_x = camera_x \
                + math.cos(math.radians(camera_yaw)) * (camera_length / 2.0) \
                - math.sin(math.radians(camera_yaw)) * (camera_width / 2.0)
            camera_b_y = camera_y \
                + math.sin(math.radians(camera_yaw)) * (camera_length / 2.0) \
                + math.cos(math.radians(camera_yaw)) * (camera_width / 2.0)

            camera_c_x = camera_x \
                + math.cos(math.radians(camera_yaw)) * (camera_length / 2.0) \
                + math.sin(math.radians(camera_yaw)) * (camera_width / 2.0)
            camera_c_y = camera_y \
                + math.sin(math.radians(camera_yaw)) * (camera_length / 2.0) \
                - math.cos(math.radians(camera_yaw)) * (camera_width / 2.0)

            camera_d_x = camera_x \
                - math.cos(math.radians(camera_yaw)) * (camera_length / 2.0) \
                + math.sin(math.radians(camera_yaw)) * (camera_width / 2.0)
            camera_d_y = camera_y \
                - math.sin(math.radians(camera_yaw)) * (camera_length / 2.0) \
                - math.cos(math.radians(camera_yaw)) * (camera_width / 2.0)

            x = np.array(
                [camera_a_x, camera_b_x, camera_c_x, camera_d_x, camera_a_x])

            y = np.array(
                [camera_a_y, camera_b_y, camera_c_y, camera_d_y, camera_a_y])

            plt.plot(x, y, color="grey")

        #show cameras lens
        for camera in panoramic_system:
            camera_yaw = camera.getYaw()
            camera_length = camera.getLength()
            camera_lens_diameter, camera_lens_length = camera.getLensSize()

            lens_center_coordinates_x = camera.getCoordinatesX() + (
                camera_length + camera_lens_length) / 2.0 * math.cos(
                    math.radians(camera_yaw))
            lens_center_coordinates_y = camera.getCoordinatesY() + (
                camera_length + camera_lens_length) / 2.0 * math.sin(
                    math.radians(camera_yaw))
            lens_a_x = lens_center_coordinates_x \
                - math.cos(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                - math.sin(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)
            lens_a_y = lens_center_coordinates_y \
                - math.sin(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                + math.cos(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)

            lens_b_x = lens_center_coordinates_x\
                + math.cos(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                - math.sin(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)
            lens_b_y = lens_center_coordinates_y \
                + math.sin(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                + math.cos(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)

            lens_c_x = lens_center_coordinates_x \
                + math.cos(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                + math.sin(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)
            lens_c_y = lens_center_coordinates_y \
                + math.sin(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                - math.cos(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)

            lens_d_x = lens_center_coordinates_x \
                - math.cos(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                + math.sin(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)
            lens_d_y = lens_center_coordinates_y \
                - math.sin(math.radians(camera_yaw)) * (camera_lens_length / 2.0) \
                - math.cos(math.radians(camera_yaw)) * (camera_lens_diameter / 2.0)

            x = np.array([lens_a_x, lens_b_x, lens_c_x, lens_d_x, lens_a_x])

            y = np.array([lens_a_y, lens_b_y, lens_c_y, lens_d_y, lens_a_y])

            plt.plot(x, y, color="grey")

        #show cameras FOV (Field of view)
        border_of_view_far = 0.0
        for camera_1 in panoramic_system:
            for camera_2 in panoramic_system:
                new_border_of_view_far = 2 * math.fabs(
                    camera_1.getCoordinatesY() - camera_2.getCoordinatesY())
                if (border_of_view_far < new_border_of_view_far):
                    border_of_view_far = new_border_of_view_far

        for camera in panoramic_system:
            camera_yaw = camera.getYaw()
            camera_length = camera.getLength()
            camera_lens_length = camera.getLensLength()
            camera_width_angle_of_view = camera.getWidthAngleOfView()

            border_of_view_close = camera_lens_length / 2.0
            small_triangle_side = border_of_view_close / math.cos(
                math.radians(camera_width_angle_of_view / 2.0))
            big_triangle_side = border_of_view_far / math.cos(
                math.radians(camera_width_angle_of_view / 2.0))

            lens_center_x = camera.getCoordinatesX() + (
                camera_length + camera_lens_length) / 2.0 * math.cos(
                    math.radians(camera_yaw))
            lens_center_y = camera.getCoordinatesY() + (
                camera_length + camera_lens_length) / 2.0 * math.sin(
                    math.radians(camera_yaw))

            fov_b_x = lens_center_x + \
                big_triangle_side * math.cos(math.radians(camera_yaw + camera_width_angle_of_view / 2.0))
            fov_c_x = lens_center_x + \
                big_triangle_side * math.cos(math.radians(camera_yaw - camera_width_angle_of_view / 2.0))
            fov_b_y = lens_center_y + \
                big_triangle_side * math.sin(math.radians(camera_yaw + camera_width_angle_of_view / 2.0))
            fov_c_y = lens_center_y + \
                big_triangle_side * math.sin(math.radians(camera_yaw - camera_width_angle_of_view / 2.0))

            fov_a_x = lens_center_x + \
                small_triangle_side * math.cos(math.radians(camera_yaw + camera_width_angle_of_view / 2.0))
            fov_d_x = lens_center_x + \
                small_triangle_side * math.cos(math.radians(camera_yaw - camera_width_angle_of_view / 2.0))
            fov_a_y = lens_center_y + \
                small_triangle_side * math.sin(math.radians(camera_yaw + camera_width_angle_of_view / 2.0))
            fov_d_y = lens_center_y + \
                small_triangle_side * math.sin(math.radians(camera_yaw - camera_width_angle_of_view / 2.0))

            x = np.array([fov_a_x, fov_b_x, fov_c_x, fov_d_x, fov_a_x])
            y = np.array([fov_a_y, fov_b_y, fov_c_y, fov_d_y, fov_a_y])
            plt.plot(x, y, color="blue")

        plt.xlabel('x, mm')
        plt.ylabel('y, mm')

        plt.grid()
        plt.show()
