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
"""This module contains functions for interacting with files and data in JSON-format.
"""

import json

import camera as cmr
import field as fld
import panoramic_system as pano


def fileReader(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data


def fileLoader(file_name, data):
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)


def saveDump(data):
    with open('dump/dump.json', "w") as write_file:
        json.dump(data, write_file)


def loadDump():
    with open('dump/dump.json', "r") as read_file:
        data = json.load(read_file)
    return data


def loadFromDumpToFile(file_name):
    with open('dump/dump.json', "r") as read_file:
        data = json.load(read_file)

    with open(file_name, "w") as write_file:
        json.dump(data, write_file)


def fieldReader(data_field):
    field_length = data_field['size']['length']
    field_width = data_field['size']['width']
    field_x = data_field['coordinates']['x']
    field_y = data_field['coordinates']['y']
    field_grandstand_width = data_field['grandstand_width']

    field = fld.Field(field_length, field_width, field_x, field_y,
                      field_grandstand_width)
    return field


def listOfPanoramicSystemsReader(panoramic_systems, data_list):
    list_of_panoramic_systems = data_list['list_of_panoramic_systems']
    for ipanoramic_system in list_of_panoramic_systems:
        panoramic_system = pano.PanoramicSystem(
            ipanoramic_system['id'], ipanoramic_system['size']['length'],
            ipanoramic_system['size']['width'],
            ipanoramic_system['size']['height'],
            ipanoramic_system['coordinates']['x'],
            ipanoramic_system['coordinates']['y'],
            ipanoramic_system['coordinates']['z'],
            ipanoramic_system['axis']['pitch'],
            ipanoramic_system['axis']['yaw'], ipanoramic_system['axis']['roll'])

        panoramic_systems.addPanoramicSystem(panoramic_system)

        for icamera in ipanoramic_system['list_of_cameras']:
            camera = cmr.Camera(
                icamera['id'], icamera['lens']['focal_length'],
                icamera['lens']['f_number'], icamera['lens']['focus_distance'],
                icamera['lens']['diameter'], icamera['lens']['length'],
                icamera['image_sensor']['width'],
                icamera['image_sensor']['height'],
                icamera['image_sensor']['pixel_size'],
                icamera['size']['length'], icamera['size']['width'],
                icamera['size']['height'], icamera['coordinates']['x'],
                icamera['coordinates']['y'], icamera['coordinates']['z'],
                icamera['axis']['pitch'], icamera['axis']['yaw'],
                icamera['axis']['roll'])

            panoramic_system.addCamera(camera)


def initModel(field_file, list_of_panoramic_systems_file):
    data_field = fileReader(field_file)
    data_list = fileReader(list_of_panoramic_systems_file)

    field = fieldReader(data_field)

    panoramic_systems = pano.ListOfPanoramicSystems()

    listOfPanoramicSystemsReader(panoramic_systems, data_list)

    return field, panoramic_systems
