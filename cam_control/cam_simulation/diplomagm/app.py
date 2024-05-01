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

from decimal import Decimal
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QListWidget, QMessageBox, QDialog, QTreeView
from PySide6.QtGui import QFont, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QStandardItemModel, QStandardItem
from PySide6.QtCore import QRegularExpression

from field_dialog import Ui_field_dialog
from pano_dialog import Ui_pano_dialog
from camera_dialog import Ui_camera_dialog
from ui_main import Ui_MainWindow
import json

import panoramic_system as pano
import json_reader
import scheme


class FieldDialog(QDialog):

    def __init__(self, parent=None):
        super(FieldDialog, self).__init__(parent)
        self.field_dialog = Ui_field_dialog()
        self.field_dialog.setupUi(self)

        self.field_file = ''

        self.field_dialog.field_save_button.clicked.connect(self.saveFieldInfo)
        self.field_dialog.field_save_as_button.clicked.connect(
            self.saveAsFieldInfo)
        self.field_dialog.field_close_button.clicked.connect(self.dialogClose)

    def defaultSpinBoxes(self):
        self.field_dialog.field_coordinates_x_spin_box.setValue(0.0)
        self.field_dialog.field_coordinates_y_spin_box.setValue(0.0)

        self.field_dialog.field_size_length_spin_box.setValue(0.0)
        self.field_dialog.field_size_width_spin_box.setValue(0.0)

        self.field_dialog.field_grandstand_spin_box.setValue(0.0)

    def saveFieldInfo(self):
        field_data = {
            "size": {
                "length": self.field_dialog.field_size_length_spin_box.value(),
                "width": self.field_dialog.field_size_width_spin_box.value()
            },
            "coordinates": {
                "x": self.field_dialog.field_coordinates_x_spin_box.value(),
                "y": self.field_dialog.field_coordinates_y_spin_box.value()
            },
            "grandstand_width":
                self.field_dialog.field_grandstand_spin_box.value()
        }

        if (self.field_file == ''):
            field_file, _ = QFileDialog.getSaveFileName(self,
                                                        'Сохранение файла', '',
                                                        'JSON file (*.json)')
            if (field_file != ''):
                json_reader.fileLoader(field_file, field_data)
                self.field_file = ''
                self.dialogClose()
        else:
            json_reader.fileLoader(self.field_file, field_data)
            self.field_file = ''
            self.dialogClose()

    def saveAsFieldInfo(self):
        field_data = {
            "size": {
                "length": self.field_dialog.field_size_length_spin_box.value(),
                "width": self.field_dialog.field_size_width_spin_box.value()
            },
            "coordinates": {
                "x": self.field_dialog.field_coordinates_x_spin_box.value(),
                "y": self.field_dialog.field_coordinates_y_spin_box.value()
            },
            "grandstand_width":
                self.field_dialog.field_grandstand_spin_box.value()
        }
        field_file, _ = QFileDialog.getSaveFileName(self, 'Сохранение файла',
                                                    '', 'JSON file (*.json)')
        if (field_file != ''):
            json_reader.fileLoader(field_file, field_data)
            self.field_file = ''
            self.dialogClose()

    def loadJsonFile(self):
        field_file, _ = QFileDialog.getOpenFileName(self, 'Выбор файла', '',
                                                    'JSON file (*.json)')
        if (field_file != ''):
            self.field_file = field_file
            data_field = json_reader.fileReader(field_file)

            self.field_dialog.field_coordinates_x_spin_box.setValue(
                data_field['coordinates']['x'])
            self.field_dialog.field_coordinates_y_spin_box.setValue(
                data_field['coordinates']['y'])

            self.field_dialog.field_size_length_spin_box.setValue(
                data_field['size']['length'])
            self.field_dialog.field_size_width_spin_box.setValue(
                data_field['size']['width'])

            self.field_dialog.field_grandstand_spin_box.setValue(
                data_field['grandstand_width'])

    def dialogClose(self):
        self.field_file = ''
        self.close()


class createCameraDialog(QDialog):

    def __init__(self, parent=None):
        super(createCameraDialog, self).__init__(parent)
        self.camera_dialog = Ui_camera_dialog()
        self.camera_dialog.setupUi(self)
        self.pano_id = 0

        self.camera_dialog.camera_create_button.clicked.connect(
            self.saveCameraInfo)
        self.camera_dialog.camera_close_button.clicked.connect(self.dialogClose)

    def defaultSpinBoxes(self, pano_id):
        self.pano_id = pano_id
        self.camera_dialog.camera_coordinates_x_spin_box.setValue(0.0)
        self.camera_dialog.camera_coordinates_y_spin_box.setValue(0.0)
        self.camera_dialog.camera_coordinates_z_spin_box.setValue(0.0)

        self.camera_dialog.camera_axis_pitch_spin_box.setValue(0.0)
        self.camera_dialog.camera_axis_yaw_spin_box.setValue(0.0)
        self.camera_dialog.camera_axis_roll_spin_box.setValue(0.0)

        self.camera_dialog.camera_size_length_spin_box.setValue(0.0)
        self.camera_dialog.camera_size_width_spin_box.setValue(0.0)
        self.camera_dialog.camera_size_height_spin_box.setValue(0.0)

        self.camera_dialog.camera_lens_focal_length_spin_box.setValue(0.0)
        self.camera_dialog.camera_lens_f_number_spin_box.setValue(1.0)
        self.camera_dialog.camera_lens_focus_distance_spin_box.setValue(0.0)
        self.camera_dialog.camera_lens_diameter_spin_box.setValue(0.0)
        self.camera_dialog.camera_lens_length_spin_box.setValue(0.0)

        self.camera_dialog.camera_image_sensor_width_spin_box.setValue(0.0)
        self.camera_dialog.camera_image_sensor_height_spin_box.setValue(0.0)
        self.camera_dialog.camera_image_sensor_pixel_size_spin_box.setValue(0.0)

    def saveCameraInfo(self):
        data_list = json_reader.loadDump()
        camera_data = {
            'id':
                len(data_list['list_of_panoramic_systems'][self.pano_id]
                    ['list_of_cameras']),
            'coordinates': {
                'x': self.camera_dialog.camera_coordinates_x_spin_box.value(),
                'y': self.camera_dialog.camera_coordinates_y_spin_box.value(),
                'z': self.camera_dialog.camera_coordinates_z_spin_box.value()
            },
            'axis': {
                'pitch': self.camera_dialog.camera_axis_pitch_spin_box.value(),
                'yaw': self.camera_dialog.camera_axis_yaw_spin_box.value(),
                'roll': self.camera_dialog.camera_axis_roll_spin_box.value()
            },
            'size': {
                'length':
                    self.camera_dialog.camera_size_length_spin_box.value(),
                'width':
                    self.camera_dialog.camera_size_width_spin_box.value(),
                'height':
                    self.camera_dialog.camera_size_height_spin_box.value()
            },
            'lens': {
                'focal_length':
                    self.camera_dialog.camera_lens_focal_length_spin_box.value(
                    ),
                'f_number':
                    self.camera_dialog.camera_lens_f_number_spin_box.value(),
                'focus_distance':
                    self.camera_dialog.camera_lens_focus_distance_spin_box.
                    value(),
                'diameter':
                    self.camera_dialog.camera_lens_diameter_spin_box.value(),
                'length':
                    self.camera_dialog.camera_lens_length_spin_box.value()
            },
            'image_sensor': {
                'width':
                    self.camera_dialog.camera_image_sensor_width_spin_box.value(
                    ),
                'height':
                    self.camera_dialog.camera_image_sensor_height_spin_box.
                    value(),
                'pixel_size':
                    self.camera_dialog.camera_image_sensor_pixel_size_spin_box.
                    value()
            }
        }

        data_list['list_of_panoramic_systems'][
            self.pano_id]['list_of_cameras'].append(camera_data)
        json_reader.saveDump(data_list)
        self.close()

    def dialogClose(self):
        self.close()

    def dialogClose(self):
        self.close()


class changeCameraDialog(QDialog):

    def __init__(self, parent=None):
        super(changeCameraDialog, self).__init__(parent)
        self.camera_dialog = Ui_camera_dialog()
        self.camera_dialog.setupUi(self)
        self.pano_id = 0
        self.camera_id = 0

        self.camera_dialog.camera_create_button.setText('Изменить')
        self.camera_dialog.camera_create_button.clicked.connect(
            self.saveCameraInfo)
        self.camera_dialog.camera_close_button.clicked.connect(self.dialogClose)

    def setSpinBoxes(self, pano_id, camera_id):
        self.pano_id = pano_id
        self.camera_id = camera_id
        data_list = json_reader.loadDump()
        self.camera_dialog.camera_coordinates_x_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['coordinates']['x'])
        self.camera_dialog.camera_coordinates_y_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['coordinates']['y'])
        self.camera_dialog.camera_coordinates_z_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['coordinates']['z'])

        self.camera_dialog.camera_axis_pitch_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['axis']['pitch'])
        self.camera_dialog.camera_axis_yaw_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['axis']['yaw'])
        self.camera_dialog.camera_axis_roll_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['axis']['roll'])

        self.camera_dialog.camera_size_length_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['size']['length'])
        self.camera_dialog.camera_size_width_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['size']['width'])
        self.camera_dialog.camera_size_height_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['size']['height'])

        self.camera_dialog.camera_lens_focal_length_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['lens']['focal_length'])
        self.camera_dialog.camera_lens_f_number_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['lens']['f_number'])
        self.camera_dialog.camera_lens_focus_distance_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['lens']['focus_distance'])
        self.camera_dialog.camera_lens_diameter_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['lens']['diameter'])
        self.camera_dialog.camera_lens_length_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['lens']['length'])

        self.camera_dialog.camera_image_sensor_width_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['image_sensor']['width'])
        self.camera_dialog.camera_image_sensor_height_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['image_sensor']['height'])
        self.camera_dialog.camera_image_sensor_pixel_size_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['list_of_cameras']
            [camera_id]['image_sensor']['pixel_size'])

    def saveCameraInfo(self):
        data_list = json_reader.loadDump()
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['coordinates'][
                'x'] = self.camera_dialog.camera_coordinates_x_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['coordinates'][
                'y'] = self.camera_dialog.camera_coordinates_y_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['coordinates'][
                'z'] = self.camera_dialog.camera_coordinates_z_spin_box.value()

        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['axis'][
                'pitch'] = self.camera_dialog.camera_axis_pitch_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['axis'][
                'yaw'] = self.camera_dialog.camera_axis_yaw_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['axis'][
                'roll'] = self.camera_dialog.camera_axis_roll_spin_box.value()

        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['size'][
                'length'] = self.camera_dialog.camera_size_length_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['size'][
                'width'] = self.camera_dialog.camera_size_width_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['size'][
                'height'] = self.camera_dialog.camera_size_height_spin_box.value(
                )

        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['lens'][
                'focal_length'] = self.camera_dialog.camera_lens_focal_length_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['lens'][
                'f_number'] = self.camera_dialog.camera_lens_f_number_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['lens'][
                'focus_distance'] = self.camera_dialog.camera_lens_focus_distance_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['lens'][
                'diameter'] = self.camera_dialog.camera_lens_diameter_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['lens'][
                'length'] = self.camera_dialog.camera_lens_length_spin_box.value(
                )

        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['image_sensor'][
                'width'] = self.camera_dialog.camera_image_sensor_width_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['image_sensor'][
                'height'] = self.camera_dialog.camera_image_sensor_height_spin_box.value(
                )
        data_list['list_of_panoramic_systems'][self.pano_id]['list_of_cameras'][
            self.camera_id]['image_sensor'][
                'pixel_size'] = self.camera_dialog.camera_image_sensor_pixel_size_spin_box.value(
                )
        json_reader.saveDump(data_list)
        self.close()

    def dialogClose(self):
        self.close()


class createPanoDialog(QDialog):

    def __init__(self, parent=None):
        super(createPanoDialog, self).__init__(parent)
        self.pano_dialog = Ui_pano_dialog()
        self.pano_dialog.setupUi(self)

        self.pano_dialog.pano_create_button.clicked.connect(self.savePanoInfo)
        self.pano_dialog.pano_close_button.clicked.connect(self.dialogClose)

    def defaultSpinBoxes(self):
        self.pano_dialog.pano_coordinates_x_spin_box.setValue(0.0)
        self.pano_dialog.pano_coordinates_y_spin_box.setValue(0.0)
        self.pano_dialog.pano_coordinates_z_spin_box.setValue(0.0)

        self.pano_dialog.pano_axis_pitch_spin_box.setValue(0.0)
        self.pano_dialog.pano_axis_yaw_spin_box.setValue(0.0)
        self.pano_dialog.pano_axis_roll_spin_box.setValue(0.0)

        self.pano_dialog.pano_size_length_spin_box.setValue(0.0)
        self.pano_dialog.pano_size_width_spin_box.setValue(0.0)
        self.pano_dialog.pano_size_height_spin_box.setValue(0.0)

    def savePanoInfo(self):
        data_list = json_reader.loadDump()
        pano_data = {
            'id': len(data_list['list_of_panoramic_systems']),
            'coordinates': {
                'x': self.pano_dialog.pano_coordinates_x_spin_box.value(),
                'y': self.pano_dialog.pano_coordinates_y_spin_box.value(),
                'z': self.pano_dialog.pano_coordinates_z_spin_box.value()
            },
            'axis': {
                'pitch': self.pano_dialog.pano_axis_pitch_spin_box.value(),
                'yaw': self.pano_dialog.pano_axis_yaw_spin_box.value(),
                'roll': self.pano_dialog.pano_axis_roll_spin_box.value()
            },
            'size': {
                'length': self.pano_dialog.pano_size_length_spin_box.value(),
                'width': self.pano_dialog.pano_size_width_spin_box.value(),
                'height': self.pano_dialog.pano_size_height_spin_box.value()
            },
            'list_of_cameras': []
        }

        data_list['list_of_panoramic_systems'].append(pano_data)
        json_reader.saveDump(data_list)
        self.close()

    def dialogClose(self):
        self.close()


class changePanoDialog(QDialog):

    def __init__(self, parent=None):
        super(changePanoDialog, self).__init__(parent)
        self.pano_id = 0
        self.pano_dialog = Ui_pano_dialog()
        self.pano_dialog.setupUi(self)

        self.pano_dialog.pano_create_button.setText('Изменить')
        self.pano_dialog.pano_create_button.clicked.connect(self.savePanoInfo)
        self.pano_dialog.pano_close_button.clicked.connect(self.dialogClose)

    def setSpinBoxes(self, pano_id):
        self.pano_id = pano_id
        data_list = json_reader.loadDump()
        self.pano_dialog.pano_coordinates_x_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['coordinates']['x'])
        self.pano_dialog.pano_coordinates_y_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['coordinates']['y'])
        self.pano_dialog.pano_coordinates_z_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['coordinates']['z'])

        self.pano_dialog.pano_axis_pitch_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['axis']['pitch'])
        self.pano_dialog.pano_axis_yaw_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['axis']['yaw'])
        self.pano_dialog.pano_axis_roll_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['axis']['roll'])

        self.pano_dialog.pano_size_length_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['size']['length'])
        self.pano_dialog.pano_size_width_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['size']['width'])
        self.pano_dialog.pano_size_height_spin_box.setValue(
            data_list['list_of_panoramic_systems'][pano_id]['size']['height'])

    def savePanoInfo(self):
        data_list = json_reader.loadDump()
        data_list['list_of_panoramic_systems'][self.pano_id]['coordinates'][
            'x'] = self.pano_dialog.pano_coordinates_x_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['coordinates'][
            'y'] = self.pano_dialog.pano_coordinates_y_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['coordinates'][
            'z'] = self.pano_dialog.pano_coordinates_z_spin_box.value()

        data_list['list_of_panoramic_systems'][self.pano_id]['axis'][
            'pitch'] = self.pano_dialog.pano_axis_pitch_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['axis'][
            'yaw'] = self.pano_dialog.pano_axis_yaw_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['axis'][
            'roll'] = self.pano_dialog.pano_axis_roll_spin_box.value()

        data_list['list_of_panoramic_systems'][self.pano_id]['size'][
            'length'] = self.pano_dialog.pano_size_length_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['size'][
            'width'] = self.pano_dialog.pano_size_width_spin_box.value()
        data_list['list_of_panoramic_systems'][self.pano_id]['size'][
            'height'] = self.pano_dialog.pano_size_height_spin_box.value()
        json_reader.saveDump(data_list)
        self.close()

    def dialogClose(self):
        self.close()


class ExpenseTracker(QMainWindow):

    def __init__(self):
        super(ExpenseTracker, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.data_list = {}
        json_reader.saveDump(self.data_list)

        self.pano_combo_box_list = ['']
        self.ui.pano_combo_box.addItems(self.pano_combo_box_list)
        self.ui.pano_combo_box.currentTextChanged.connect(
            self.cameraComboBoxUpdate)

        self.camera_combo_box_list = ['']
        self.ui.camera_combo_box.addItems(self.camera_combo_box_list)

        self.panoComboBoxUpdate()
        self.cameraComboBoxUpdate()
        self.allButtonsUpdate()

        self.field_window = FieldDialog(parent=self)
        self.pano_create_window = createPanoDialog(parent=self)
        self.pano_change_window = changePanoDialog(parent=self)
        self.camera_create_window = createCameraDialog(parent=self)
        self.camera_change_window = changeCameraDialog(parent=self)

        self.ui.pano_list_tree.setHeaderHidden(True)

        self.ui.pano_add_button.clicked.connect(self.panoDialogAdd)
        self.ui.pano_change_button.clicked.connect(self.panoDialogChange)
        self.ui.pano_remove_button.clicked.connect(self.panoDialogRemove)

        self.ui.pano_list_create_button.clicked.connect(self.panoListCreate)
        self.ui.pano_list_load_button.clicked.connect(
            self.panoListLoadFromJsonFile)
        self.ui.pano_list_clear_button.clicked.connect(self.panoListRemove)
        self.ui.pano_list_save_button.clicked.connect(self.panoListSave)
        self.ui.pano_list_save_as_button.clicked.connect(self.panoListSaveAs)

        self.ui.camera_add_button.clicked.connect(self.cameraDialogAdd)
        self.ui.camera_change_button.clicked.connect(self.cameraDialogChange)
        self.ui.camera_remove_button.clicked.connect(self.cameraDialogRemove)

        self.ui.field_create_button.clicked.connect(self.fieldDialogStart)
        self.ui.field_load_button.clicked.connect(
            self.fieldDialogLoadFromJsonFile)

        self.ui.field_file_button.clicked.connect(self.fieldSearchFileName)
        self.ui.pano_file_button.clicked.connect(self.panoListSearchFileName)
        self.ui.create_FOV_button.clicked.connect(self.start_FOV)
        self.ui.create_DOF_button.clicked.connect(self.start_DOF)

    def fieldDialogStart(self):
        self.field_window.defaultSpinBoxes()
        self.field_window.exec()

    def panoDialogAdd(self):
        self.pano_create_window.defaultSpinBoxes()
        self.pano_create_window.exec()
        self.data_list = json_reader.loadDump()
        self.panoComboBoxUpdate()
        self.allButtonsUpdate()
        self.treeUpdate()

    def panoDialogChange(self):
        pano_id = int(self.ui.pano_combo_box.currentText())
        self.pano_change_window.setSpinBoxes(pano_id)
        self.pano_change_window.exec()
        self.data_list = json_reader.loadDump()
        #self.panoComboBoxUpdate()
        self.allButtonsUpdate()
        #self.treeUpdate()

    def panoDialogRemove(self):
        pano_id = int(self.ui.pano_combo_box.currentText())
        self.data_list['list_of_panoramic_systems'].pop(pano_id)
        i = 0
        for ipano in self.data_list['list_of_panoramic_systems']:
            ipano['id'] = i
            i = i + 1
        json_reader.saveDump(self.data_list)
        self.panoComboBoxUpdate()
        self.allButtonsUpdate()
        self.treeUpdate()

    def cameraDialogAdd(self):
        pano_id = int(self.ui.pano_combo_box.currentText())
        self.camera_create_window.defaultSpinBoxes(pano_id)
        self.camera_create_window.exec()
        self.data_list = json_reader.loadDump()
        self.cameraComboBoxUpdate()
        self.allButtonsUpdate()
        self.treeUpdate()

    def cameraDialogChange(self):
        pano_id = int(self.ui.pano_combo_box.currentText())
        camera_id = int(self.ui.camera_combo_box.currentText())
        self.camera_change_window.setSpinBoxes(pano_id, camera_id)
        self.camera_change_window.exec()
        self.data_list = json_reader.loadDump()
        #self.cameraComboBoxUpdate()
        self.allButtonsUpdate()
        #self.treeUpdate()

    def cameraDialogRemove(self):
        pano_id = int(self.ui.pano_combo_box.currentText())
        camera_id = int(self.ui.camera_combo_box.currentText())
        self.data_list['list_of_panoramic_systems'][pano_id][
            'list_of_cameras'].pop(camera_id)
        i = 0
        for icamera in self.data_list['list_of_panoramic_systems'][pano_id][
                'list_of_cameras']:
            icamera['id'] = i
            i = i + 1
        json_reader.saveDump(self.data_list)
        self.cameraComboBoxUpdate()
        self.allButtonsUpdate()
        self.treeUpdate()

    def cameraDialogCreate(self):
        self.camera_window.defaultSpinBoxes()
        self.camera_window.exec()

    def fieldDialogLoadFromJsonFile(self):
        self.field_window.loadJsonFile()
        self.field_window.exec()

    def treeUpdate(self):
        self.tree_model = QStandardItemModel()
        self.tree_root = self.tree_model.invisibleRootItem()

        if (self.data_list != {}):
            self.tree_list_pano = QStandardItem('List of panoramic systems')
            self.tree_list_pano.setEditable(False)
            self.tree_root.appendRow(self.tree_list_pano)

            for ipano in self.data_list['list_of_panoramic_systems']:
                ipano_item = QStandardItem('Panoramic system ' +
                                           str(ipano['id']))
                ipano_item.setData(ipano['id'])
                ipano_item.setEditable(False)
                self.tree_list_pano.appendRow(ipano_item)
                icamera_list = []

                for icamera in ipano['list_of_cameras']:
                    icamera_item = QStandardItem('Camera ' + str(icamera['id']))
                    icamera_item.setData(ipano['id'])
                    icamera_item.setEditable(False)
                    icamera_list.append(icamera_item)

                ipano_item.appendRows(icamera_list)

        self.ui.pano_list_tree.setModel(self.tree_model)
        self.ui.pano_list_tree.expandAll()

    def panoComboBoxUpdate(self):
        self.pano_combo_box_list.clear()

        if (self.data_list == {}):
            self.pano_combo_box_list.append('')
        elif (len(self.data_list['list_of_panoramic_systems']) == 0):
            self.pano_combo_box_list.append('')
        else:
            for ipano in self.data_list['list_of_panoramic_systems']:
                self.pano_combo_box_list.append(str(ipano['id']))

        if (self.data_list == {}):
            self.ui.pano_combo_box.setEnabled(False)
        else:
            self.ui.pano_combo_box.setEnabled(True)

        self.ui.pano_combo_box.clear()
        self.ui.pano_combo_box.addItems(self.pano_combo_box_list)

    def cameraComboBoxUpdate(self):
        self.camera_combo_box_list.clear()

        if (self.data_list == {}):
            self.camera_combo_box_list.append('')
        elif (len(self.data_list['list_of_panoramic_systems']) == 0):
            self.camera_combo_box_list.append('')
        elif (self.ui.pano_combo_box.currentText() == ''):
            self.camera_combo_box_list.append('')
        else:
            pano_id = int(self.ui.pano_combo_box.currentText())
            if (len(self.data_list['list_of_panoramic_systems'][pano_id]
                    ['list_of_cameras']) == 0):
                self.camera_combo_box_list.append('')
            else:
                for icamera in self.data_list['list_of_panoramic_systems'][
                        pano_id]['list_of_cameras']:
                    self.camera_combo_box_list.append(str(icamera['id']))

        if (self.data_list == {}):
            self.ui.camera_combo_box.setEnabled(False)
        elif (len(self.data_list['list_of_panoramic_systems']) == 0):
            self.ui.camera_combo_box.setEnabled(False)
        else:
            self.ui.camera_combo_box.setEnabled(True)

        self.ui.camera_combo_box.clear()
        self.ui.camera_combo_box.addItems(self.camera_combo_box_list)

    def panoButtonsUpdate(self):
        if (self.data_list == {}):
            self.ui.pano_add_button.setEnabled(False)
            self.ui.pano_change_button.setEnabled(False)
            self.ui.pano_remove_button.setEnabled(False)
        elif (len(self.data_list['list_of_panoramic_systems']) == 0):
            self.ui.pano_add_button.setEnabled(True)
            self.ui.pano_change_button.setEnabled(False)
            self.ui.pano_remove_button.setEnabled(False)
        else:
            self.ui.pano_add_button.setEnabled(True)
            self.ui.pano_change_button.setEnabled(True)
            self.ui.pano_remove_button.setEnabled(True)

    def cameraButtonsUpdate(self):
        if (self.data_list == {}):
            self.ui.camera_add_button.setEnabled(False)
            self.ui.camera_change_button.setEnabled(False)
            self.ui.camera_remove_button.setEnabled(False)
        elif (len(self.data_list['list_of_panoramic_systems']) == 0):
            self.ui.camera_add_button.setEnabled(False)
            self.ui.camera_change_button.setEnabled(False)
            self.ui.camera_remove_button.setEnabled(False)
        else:
            pano_id = int(self.ui.pano_combo_box.currentText())
            if (len(self.data_list['list_of_panoramic_systems'][pano_id]
                    ['list_of_cameras']) == 0):
                self.ui.camera_add_button.setEnabled(True)
                self.ui.camera_change_button.setEnabled(False)
                self.ui.camera_remove_button.setEnabled(False)
            else:
                self.ui.camera_add_button.setEnabled(True)
                self.ui.camera_change_button.setEnabled(True)
                self.ui.camera_remove_button.setEnabled(True)

    def panoListButtonsUpdate(self):
        if (self.data_list == {}):
            self.ui.pano_list_save_button.setEnabled(False)
            self.ui.pano_list_save_as_button.setEnabled(False)
            self.ui.pano_list_create_button.setEnabled(True)
            self.ui.pano_list_load_button.setEnabled(True)
            self.ui.pano_list_clear_button.setEnabled(False)
        else:
            self.ui.pano_list_save_button.setEnabled(True)
            self.ui.pano_list_save_as_button.setEnabled(True)
            self.ui.pano_list_create_button.setEnabled(False)
            self.ui.pano_list_load_button.setEnabled(False)
            self.ui.pano_list_clear_button.setEnabled(True)

    def allButtonsUpdate(self):
        self.panoListButtonsUpdate()
        self.panoButtonsUpdate()
        self.cameraButtonsUpdate()

    def panoListCreate(self):
        self.data_list = {'list_of_panoramic_systems': []}
        json_reader.saveDump(self.data_list)
        self.panoComboBoxUpdate()
        self.allButtonsUpdate()
        self.treeUpdate()

    def panoListLoadFromJsonFile(self):
        pano_list_file, _ = QFileDialog.getOpenFileName(self, 'Выбор файла', '',
                                                        'JSON file (*.json)')
        if (pano_list_file != ''):
            self.ui.pano_list_file_line.setText(pano_list_file)
            self.data_list = json_reader.fileReader(pano_list_file)
            json_reader.saveDump(self.data_list)
            self.panoComboBoxUpdate()
            self.cameraComboBoxUpdate()
            self.allButtonsUpdate()
            self.treeUpdate()

    def panoListRemove(self):
        self.data_list = {}
        json_reader.saveDump(self.data_list)
        self.ui.pano_list_file_line.setText('')
        self.allButtonsUpdate()
        self.panoComboBoxUpdate()
        self.cameraComboBoxUpdate()
        self.treeUpdate()

    def panoListSave(self):
        if (self.ui.pano_list_file_line.text() == ''):
            pano_list_file, _ = QFileDialog.getSaveFileName(
                self, 'Сохранение файла', '', 'JSON file (*.json)')

            if (pano_list_file != ''):
                self.ui.pano_list_save_button.setEnabled(False)
                self.ui.pano_list_file_line.setText(pano_list_file)
                json_reader.loadFromDumoToFile(pano_list_file)
        else:
            self.ui.pano_list_save_button.setEnabled(False)
            json_reader.loadFromDumpToFile(self.ui.pano_list_file_line.text())

    def panoListSaveAs(self):
        pano_list_file, _ = QFileDialog.getSaveFileName(self,
                                                        'Сохранение файла', '',
                                                        'JSON file (*.json)')
        if (pano_list_file != ''):
            self.ui.pano_list_save_button.setEnabled(False)
            self.ui.pano_list_file_line.setText(pano_list_file)
            json_reader.loadFromDumpToFile(pano_list_file)

    def fieldSearchFileName(self):
        field_file, _ = QFileDialog.getOpenFileName(self, 'Выбор файла', '',
                                                    'JSON file (*.json)')
        if (field_file != ''):
            self.ui.field_search_file_line.setText(field_file)

    def panoListSearchFileName(self):
        pano_list_file, _ = QFileDialog.getOpenFileName(self, 'Выбор файла', '',
                                                        'JSON file (*.json)')
        if (pano_list_file != ''):
            self.ui.pano_search_file_line.setText(pano_list_file)

    def start_FOV(self):
        if (self.ui.field_search_file_line.text() == ''):
            self.ui.create_FOV_error_label.setText(
                'Выберите футбольное поле...')
        elif (self.ui.pano_search_file_line.text() == ''):
            self.ui.create_FOV_error_label.setText(
                'Выберите список панорамных систем...')
        else:
            self.ui.create_FOV_error_label.clear()
            field, list_of_panoramic_systems = json_reader.initModel(
                self.ui.field_search_file_line.text(),
                self.ui.pano_search_file_line.text())

            #list_of_panoramic_systems.printParameters()
            #list_of_panoramic_systems.printFieldOfView()

            scheme.showFOV(field, list_of_panoramic_systems)

    def start_DOF(self):
        if (self.ui.field_search_file_line.text() == ''):
            self.ui.create_DOF_error_label.setText(
                'Выберите футбольное поле...')
        elif (self.ui.pano_search_file_line.text() == ''):
            self.ui.create_DOF_error_label.setText(
                'Выберите список панорамных систем...')
        else:
            self.ui.create_DOF_error_label.clear()
            field, list_of_panoramic_systems = json_reader.initModel(
                self.ui.field_search_file_line.text(),
                self.ui.pano_search_file_line.text())

            #list_of_panoramic_systems.printParameters()
            #list_of_panoramic_systems.printFieldOfView()

            scheme.showFOS(field, list_of_panoramic_systems)

    def writeFieldToJson(self):
        field_file, _ = QFileDialog.getSaveFileName(self, 'Сохранение файла',
                                                    '', 'JSON file (*.json)')
        if (field_file != ''):
            field_data = self.readField()
            with open(field_file, "w") as write_field:
                json.dump(field_data, write_field)

    def readField(self):
        data_field = {}
        data_field['size'] = {
            'length': self.ui.field_size_length_spin_box.value(),
            'width': self.ui.field_size_width_spin_box.value()
        }
        data_field['coordinates'] = {
            'x': self.ui.field_coordinates_x_spin_box.value(),
            'y': self.ui.field_coordinates_y_spin_box.value()
        }
        data_field[
            'grandstand_width'] = self.ui.field_grandstand_spin_box.value()

        return data_field
