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

import basis
"""This module contains the field class and its methods for storing, 
retrieving and changing the parameters of the areas of interest to us.
"""


class Field():

    def __init__(self, length, width, x, y, grandstand_width):
        self.__size = basis.Size(length, width)
        self.__coordinates = basis.Coordinates(x, y)
        self.__grandstand_width = grandstand_width
        self.__a_coordinates = basis.Coordinates(
            x - width / 2.0, y + length / 2.0, 0.0
        )  # panoramic system in the center of the field, field level = ground level
        self.__b_coordinates = basis.Coordinates(x + width / 2.0,
                                                 y + length / 2.0, 0.0)
        self.__c_coordinates = basis.Coordinates(x + width / 2.0,
                                                 y - length / 2.0, 0.0)
        self.__d_coordinates = basis.Coordinates(x - width / 2.0,
                                                 y - length / 2.0, 0.0)

    def getSize(self):
        return self.__size.getSize()

    def getLength(self):
        return self.__size.getLength()

    def getWidth(self):
        return self.__size.getWidth()

    def getCoordinates(self):
        return self.__coordinates.getCoordinates()

    def getCoordinatesX(self):
        return self.__coordinates.getCoordinatesX()

    def getCoordinatesY(self):
        return self.__coordinates.getCoordinatesY()

    def getGrandstandWidth(self):
        return self.__grandstand_width

    def getABCDCoordinates(self):
        return self.__a_coordinates, self.__b_coordinates, \
               self.__c_coordinates, self.__d_coordinates

    def getACoordinates(self):
        return self.__a_coordinates

    def getBCoordinates(self):
        return self.__b_coordinates

    def getCCoordinates(self):
        return self.__c_coordinates

    def getDCoordinates(self):
        return self.__d_coordinates
