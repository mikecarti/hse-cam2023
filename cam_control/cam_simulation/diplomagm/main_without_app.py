# MIT License
import json
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

import sys
from typing import List, Tuple

import numpy as np

sys.path.append("cam_control/cam_simulation/diplomagm")

from camera import Camera
from panoramic_system import PanoramicSystem
from json_reader import initModel


# from panoramic_system import ListOfPanoramicSystems, PanoramicSystem


class FOVCalculator:
    def __init__(self):
        self.path_to_folders = "cam_control/cam_simulation/diplomagm/"
        self.path_to_field = self.path_to_folders + 'fields/hse_1_camera.json'
        self.panoramic_systems = self._init_panoramic_system()

    def _init_panoramic_system(self, yaw=None, pitch=None) -> List[PanoramicSystem]:
        field, list_of_panoramic_systems = initModel(self.path_to_field,
                                                     self.path_to_folders + 'lists of panoramic systems/hse_1_camera.json')
        camera_systems = list_of_panoramic_systems.getListOfPanoramicSystems()
        if yaw is None or pitch is None:
            return camera_systems

        assert len(camera_systems) == 1, \
            f"panoramic_system length is not equal to one, expected usage with only 1 camera"
        panoramic_system = camera_systems[0]
        panoramic_system.changeProperties(id=0, pitch=pitch, yaw=yaw, roll=1e-5)
        return [panoramic_system]

    def get_points_of_fov(self, camera_properties=None):
        if camera_properties is not None:
            yaw = camera_properties.get('yaw')
            pitch = camera_properties.get('pitch')
            self.panoramic_systems = self._init_panoramic_system(yaw=yaw, pitch=pitch)
        return np.array([panoramic_system.calculatePanoramicSystemFOV() for panoramic_system in self.panoramic_systems][0])

    def get_field_size(self) -> Tuple["width", "length"]:
        f = open(self.path_to_field)
        field_info = json.load(f)
        size = field_info.get("size")
        return size.get("width"), size.get("length")

    def get_rotation_coords(self):
        system = self.panoramic_systems[0]
        return system.getYaw(), system.getPitch()