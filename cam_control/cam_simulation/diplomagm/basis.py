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
"""
Classes for basic concepts (size, coordinates, axis, tetragon, line) that are used as parameters for panoramic systems and cameras.
"""

import numpy as np


class Coordinates():
    """Class for panoramic system and camera body center coordinates.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Class constructor.

        :param x: x coordinate, defaults to 0.0
        :type x: float, optional
        :param y: y coordinate, defaults to 0.0
        :type y: float, optional
        :param z: z coordinate, defaults to 0.0
        :type z: float, optional
        """
        self.__x = x
        self.__y = y
        self.__z = z

    def getCoordinates(self):
        """Get x, y, z coordinates.

        :return: x, y, z coordinates.
        :rtype: float, optional
        """
        return self.__x, self.__y, self.__z

    def getCoordinatesX(self):
        """Get x coordinate.

        :return: x coordinate
        :rtype: float, optional
        """
        return self.__x

    def getCoordinatesY(self):
        """Get y coordinate.

        :return: y coordinate
        :rtype: float, optional
        """
        return self.__y

    def getCoordinatesZ(self):
        """Get z coordinate.

        :return: z coordinate
        :rtype: float, optional
        """
        return self.__z

    def setCoordinates(self, x=0.0, y=0.0, z=0.0):
        """Set x, y, z coordinates.

        :param x: x coordinate, defaults to 0.0
        :type x: float, optional
        :param y: y coordinate, defaults to 0.0
        :type y: float, optional
        :param z: z coordinate, defaults to 0.0
        :type z: float, optional
        """
        self.__x = x
        self.__y = y
        self.__z = z

    def setCoordinatesX(self, x=0.0):
        """Set x coordinate.

        :param x: x coordinate, defaults to 0.0
        :type x: float, optional
        """
        self.__x = x

    def setCoordinatesY(self, y=0.0):
        """Set y coordinate.

        :param y: y coordinate, defaults to 0.0
        :type y: float, optional
        """
        self.__y = y

    def setCoordinatesZ(self, z=0.0):
        """Set z coordinate.

        :param z: z coordinate, defaults to 0.0
        :type z: float, optional
        """
        self.__z = z


class Line():
    """Class for lines given by a parametric equation.
    """

    def __init__(self, point_1, point_2):
        """Class constructor.

        :param point_1: first point of line
        :type point_1: np.array
        :param point_2: second point of line
        :type point_2: np.array
        """
        self.__vector_a = point_2 - point_1
        self.__point = point_1

    def getLine(self):
        """Get guide vector and point of line.

        :return: guide vector and point of line
        :rtype: np.arrray
        """
        return self.__vector_a, self.__point

    def getVector(self):
        """Get guide vector of line.

        :return: guide vector of line
        :rtype: np.array
        """
        return self.__vector_a

    def getPoint(self):
        """Get point of line.

        :return: point of line
        :rtype: np.array
        """
        return self.__point


class Tetragon():
    """Class for cameras fields of view and sharpness.
    """

    def __init__(self,
                 a_x=0.0,
                 a_y=0.0,
                 a_z=0.0,
                 b_x=0.0,
                 b_y=0.0,
                 b_z=0.0,
                 c_x=0.0,
                 c_y=0.0,
                 c_z=0.0,
                 d_x=0.0,
                 d_y=0.0,
                 d_z=0.0):
        """Class constructor.

        :param a_x: x coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_x: float, optional
        :param a_y: y coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_y: float, optional
        :param a_z: z coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_z: float, optional
        :param b_x: x coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_x: float, optional
        :param b_y: y coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_y: float, optional
        :param b_z: z coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_z: float, optional
        :param c_x: x coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_x: float, optional
        :param c_y: y coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_y: float, optional
        :param c_z: z coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_z: float, optional
        :param d_x: x coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_x: float, optional
        :param d_y: y coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_y: float, optional
        :param d_z: z coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_z: float, optional
        """
        self.__a = Coordinates(a_x, a_y, a_z)
        self.__b = Coordinates(b_x, b_y, b_z)
        self.__c = Coordinates(c_x, c_y, c_z)
        self.__d = Coordinates(d_x, d_y, d_z)

        a = np.array([a_x, a_y, a_z])
        b = np.array([b_x, b_y, b_z])
        c = np.array([c_x, c_y, c_z])
        d = np.array([d_x, d_y, d_z])

        self.__ab = Line(a, b)
        self.__bc = Line(b, c)
        self.__cd = Line(c, d)
        self.__da = Line(d, a)

    def getLines(self):
        """Get ab, bc, cd, da lines.

        :return: ab, bc, cd, da lines.
        :rtype: class Line
        """
        return self.__ab.getVector(), self.__ab.getPoint(), self.__bc.getVector(
        ), self.__bc.getPoint(), self.__cd.getVector(), self.__cd.getPoint(
        ), self.__da.getVector(), self.__da.getPoint()

    def getVertices(self):
        """Get coordinates of a, b, c, d vertices.

        :return: coordinates of a, b, c, d vertices
        :rtype: class Coordinates
        """
        return self.__a, self.__b, self.__c, self.__d

    def getVertexA(self):
        """Get coordinates of a vertex a

        :return: coordinates of a vertex a
        :rtype: class Coordinates
        """
        return self.__a

    def getVertexB(self):
        """Get coordinates of a vertex b

        :return: coordinates of a vertex b
        :rtype: class Coordinates
        """
        return self.__b

    def getVertexC(self):
        """Get coordinates of a vertex c

        :return: coordinates of a vertex c
        :rtype: class Coordinates
        """
        return self.__c

    def getVertexD(self):
        """Get coordinates of a vertex d

        :return: coordinates of a vertex d
        :rtype: class Coordinates
        """
        return self.__d

    def setVertices(self,
                    a_x=0.0,
                    a_y=0.0,
                    a_z=0.0,
                    b_x=0.0,
                    b_y=0.0,
                    b_z=0.0,
                    c_x=0.0,
                    c_y=0.0,
                    c_z=0.0,
                    d_x=0.0,
                    d_y=0.0,
                    d_z=0.0):
        """Set new coordinates of a, b, c, d vertices.

        :param a_x: x coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_x: float, optional
        :param a_y: y coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_y: float, optional
        :param a_z: z coordinate for vertex a of a quadrilateral, defaults to 0.0
        :type a_z: float, optional
        :param b_x: x coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_x: float, optional
        :param b_y: y coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_y: float, optional
        :param b_z: z coordinate for vertex b of a quadrilateral, defaults to 0.0
        :type b_z: float, optional
        :param c_x: x coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_x: float, optional
        :param c_y: y coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_y: float, optional
        :param c_z: z coordinate for vertex c of a quadrilateral, defaults to 0.0
        :type c_z: float, optional
        :param d_x: x coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_x: float, optional
        :param d_y: y coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_y: float, optional
        :param d_z: z coordinate for vertex d of a quadrilateral, defaults to 0.0
        :type d_z: float, optional
        """

        self.__a.setCoordinates(a_x, a_y, a_z)
        self.__b.setCoordinates(b_x, b_y, b_z)
        self.__c.setCoordinates(c_x, c_y, c_z)
        self.__d.setCoordinates(d_x, d_y, d_z)


class Axis():
    """Class for angles defining panoramic systems and cameras spatial orientation.
    """

    def __init__(self, pitch=0.0, yaw=0.0, roll=0.0):
        """Class constructor.

        :param pitch: pitch angle, defaults to 0.0
        :type pitch: float, optional
        :param yaw: yaw angle, defaults to 0.0
        :type yaw: float, optional
        :param roll: roll angle, defaults to 0.0
        :type roll: float, optional
        """
        self.__pitch = pitch
        self.__yaw = yaw
        self.__roll = roll

    def getAxis(self):
        """Get pitch, yaw, roll angles.

        :return: pitch, yaw, roll angles
        :rtype: float, optional
        """
        return self.__pitch, self.__yaw, self.__roll

    def getPitch(self):
        """Get pitch angle.

        :return: pitch angle
        :rtype: float, optional
        """
        return self.__pitch

    def getYaw(self):
        """Get yaw angle.

        :return: yaw angle
        :rtype: float, optional
        """
        return self.__yaw

    def getRoll(self):
        """Get roll angle.

        :return: roll angle
        :rtype: float, optional
        """
        return self.__roll

    def setAxis(self, pitch=0.0, yaw=0.0, roll=0.0):
        """Set pitch, yaw, roll angles.

        :param pitch: pitch angle, defaults to 0.0
        :type pitch: float, optional
        :param yaw: yaw angle, defaults to 0.0
        :type yaw: float, optional
        :param roll: roll angle, defaults to 0.0
        :type roll: float, optional
        """
        self.__pitch = pitch
        self.__yaw = yaw
        self.__roll = roll

    def setAxisPitch(self, pitch=0.0):
        """Set pitch angle.

        :param pitch: pitch angle, defaults to 0.0
        :type pitch: float, optional
        """
        self.__pitch = pitch

    def setAxisYaw(self, yaw=0.0):
        """Set yaw angle.

        :param yaw: yaw angle, defaults to 0.0
        :type yaw: float, optional
        """
        self.__yaw = yaw

    def setAxisRoll(self, roll=0.0):
        """Set roll angle.

        :param roll: roll angle, defaults to 0.0
        :type roll: float, optional
        """
        self.__roll = roll

    def getAxisYaw(self):
        return self.__yaw

    def getAxisPitch(self):
        return self.__pitch


class Size():
    """Class for panoramic systems and cameras body size.
    """

    def __init__(self, length=0.0, width=0.0, height=0.0):
        """Class constructor.

        :param length: body length, defaults to 0.0
        :type length: float, optional
        :param width: body width, defaults to 0.0
        :type width: float, optional
        :param height: body height, defaults to 0.0
        :type height: float, optional
        """
        self.__length = length
        self.__width = width
        self.__height = height

    def getSize(self):
        """Get body length, width, height.

        :return: body length, width, height
        :rtype: float, optional
        """
        return self.__length, self.__width, self.__height

    def getLength(self):
        """Get body length.

        :return: body length
        :rtype: float, optional
        """
        return self.__length

    def getWidth(self):
        """Get body width.

        :return: body width
        :rtype: float, optional
        """
        return self.__width

    def getHeight(self):
        """Get body height.

        :return: body height
        :rtype: float, optional
        """
        return self.__height

    def setSize(self, length=0.0, width=0.0, height=0.0):
        """Set body length, width, height.

        :param length: body length, defaults to 0.0
        :type length: float, optional
        :param width: body width, defaults to 0.0
        :type width: float, optional
        :param height: body height, defaults to 0.0
        :type height: float, optional
        """
        self.__length = length
        self.__width = width
        self.__height = height

    def setLength(self, lenght=0.0):
        """Set body length.

        :param lenght: body length, defaults to 0.0
        :type lenght: float, optional
        """
        self.__length = length

    def setWidth(self, width=0.0):
        """Set body width.

        :param width: body width, defaults to 0.0
        :type width: float, optional
        """
        self.__width = width

    def setSize(self, height=0.0):
        """Set body height.

        :param height: body height, defaults to 0.0
        :type height: float, optional
        """
        self.__height = height
