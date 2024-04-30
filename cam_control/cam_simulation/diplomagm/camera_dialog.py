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

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime,
                            QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox,
                               QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget)


class Ui_camera_dialog(object):

    def setupUi(self, camera_dialog):
        if not camera_dialog.objectName():
            camera_dialog.setObjectName(u"camera_dialog")
        camera_dialog.resize(400, 760)
        self.layoutWidget = QWidget(camera_dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 371, 730))
        self.camera_layout = QVBoxLayout(self.layoutWidget)
        self.camera_layout.setObjectName(u"camera_layout")
        self.camera_layout.setContentsMargins(0, 0, 0, 0)
        self.camera_label = QLabel(self.layoutWidget)
        self.camera_label.setObjectName(u"camera_label")
        self.camera_label.setMinimumSize(QSize(369, 0))
        self.camera_label.setMaximumSize(QSize(369, 30))

        self.camera_layout.addWidget(self.camera_label)

        self.camera_size_layout = QVBoxLayout()
        self.camera_size_layout.setObjectName(u"camera_size_layout")
        self.camera_size_label = QLabel(self.layoutWidget)
        self.camera_size_label.setObjectName(u"camera_size_label")

        self.camera_size_layout.addWidget(self.camera_size_label)

        self.camera_size_length_layout = QHBoxLayout()
        self.camera_size_length_layout.setObjectName(
            u"camera_size_length_layout")
        self.camera_size_length_label = QLabel(self.layoutWidget)
        self.camera_size_length_label.setObjectName(u"camera_size_length_label")

        self.camera_size_length_layout.addWidget(self.camera_size_length_label)

        self.camera_size_length_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_size_length_spin_box.setObjectName(
            u"camera_size_length_spin_box")
        self.camera_size_length_spin_box.setDecimals(2)
        self.camera_size_length_spin_box.setMinimum(0.000000000000000)
        self.camera_size_length_spin_box.setMaximum(999.990000000000009)
        self.camera_size_length_spin_box.setSingleStep(0.010000000000000)
        self.camera_size_length_spin_box.setValue(0.000000000000000)

        self.camera_size_length_layout.addWidget(
            self.camera_size_length_spin_box)

        self.camera_size_layout.addLayout(self.camera_size_length_layout)

        self.camera_size_width_layout = QHBoxLayout()
        self.camera_size_width_layout.setObjectName(u"camera_size_width_layout")
        self.camera_size_width_label = QLabel(self.layoutWidget)
        self.camera_size_width_label.setObjectName(u"camera_size_width_label")

        self.camera_size_width_layout.addWidget(self.camera_size_width_label)

        self.camera_size_width_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_size_width_spin_box.setObjectName(
            u"camera_size_width_spin_box")
        self.camera_size_width_spin_box.setDecimals(2)
        self.camera_size_width_spin_box.setMinimum(0.000000000000000)
        self.camera_size_width_spin_box.setMaximum(999.990000000000009)
        self.camera_size_width_spin_box.setSingleStep(0.010000000000000)
        self.camera_size_width_spin_box.setValue(0.000000000000000)

        self.camera_size_width_layout.addWidget(self.camera_size_width_spin_box)

        self.camera_size_layout.addLayout(self.camera_size_width_layout)

        self.camera_size_height_layout = QHBoxLayout()
        self.camera_size_height_layout.setObjectName(
            u"camera_size_height_layout")
        self.camera_size_height_label = QLabel(self.layoutWidget)
        self.camera_size_height_label.setObjectName(u"camera_size_height_label")

        self.camera_size_height_layout.addWidget(self.camera_size_height_label)

        self.camera_size_height_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_size_height_spin_box.setObjectName(
            u"camera_size_height_spin_box")
        self.camera_size_height_spin_box.setDecimals(2)
        self.camera_size_height_spin_box.setMinimum(0.000000000000000)
        self.camera_size_height_spin_box.setMaximum(999.990000000000009)
        self.camera_size_height_spin_box.setSingleStep(0.010000000000000)
        self.camera_size_height_spin_box.setValue(0.000000000000000)

        self.camera_size_height_layout.addWidget(
            self.camera_size_height_spin_box)

        self.camera_size_layout.addLayout(self.camera_size_height_layout)

        self.camera_layout.addLayout(self.camera_size_layout)

        self.camera_lens_layout = QVBoxLayout()
        self.camera_lens_layout.setObjectName(u"camera_lens_layout")
        self.camera_lens_label = QLabel(self.layoutWidget)
        self.camera_lens_label.setObjectName(u"camera_lens_label")

        self.camera_lens_layout.addWidget(self.camera_lens_label)

        self.camera_lens_focal_length_layout = QHBoxLayout()
        self.camera_lens_focal_length_layout.setObjectName(
            u"camera_lens_focal_length_layout")
        self.camera_lens_focal_length_label = QLabel(self.layoutWidget)
        self.camera_lens_focal_length_label.setObjectName(
            u"camera_lens_focal_length_label")

        self.camera_lens_focal_length_layout.addWidget(
            self.camera_lens_focal_length_label)

        self.camera_lens_focal_length_spin_box = QDoubleSpinBox(
            self.layoutWidget)
        self.camera_lens_focal_length_spin_box.setObjectName(
            u"camera_lens_focal_length_spin_box")
        self.camera_lens_focal_length_spin_box.setDecimals(2)
        self.camera_lens_focal_length_spin_box.setMinimum(0.000000000000000)
        self.camera_lens_focal_length_spin_box.setMaximum(999.990000000000009)
        self.camera_lens_focal_length_spin_box.setSingleStep(0.010000000000000)
        self.camera_lens_focal_length_spin_box.setValue(0.000000000000000)

        self.camera_lens_focal_length_layout.addWidget(
            self.camera_lens_focal_length_spin_box)

        self.camera_lens_layout.addLayout(self.camera_lens_focal_length_layout)

        self.camera_lens_f_number_layout = QHBoxLayout()
        self.camera_lens_f_number_layout.setObjectName(
            u"camera_lens_f_number_layout")
        self.camera_lens_f_number_label = QLabel(self.layoutWidget)
        self.camera_lens_f_number_label.setObjectName(
            u"camera_lens_f_number_label")

        self.camera_lens_f_number_layout.addWidget(
            self.camera_lens_f_number_label)

        self.camera_lens_f_number_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_lens_f_number_spin_box.setObjectName(
            u"camera_lens_f_number_spin_box")
        self.camera_lens_f_number_spin_box.setDecimals(1)
        self.camera_lens_f_number_spin_box.setMinimum(1.000000000000000)
        self.camera_lens_f_number_spin_box.setMaximum(32.000000000000000)
        self.camera_lens_f_number_spin_box.setSingleStep(0.100000000000000)
        self.camera_lens_f_number_spin_box.setValue(1.000000000000000)

        self.camera_lens_f_number_layout.addWidget(
            self.camera_lens_f_number_spin_box)

        self.camera_lens_layout.addLayout(self.camera_lens_f_number_layout)

        self.camera_lens_focus_distance_layout = QHBoxLayout()
        self.camera_lens_focus_distance_layout.setObjectName(
            u"camera_lens_focus_distance_layout")
        self.camera_lens_focus_distance_label = QLabel(self.layoutWidget)
        self.camera_lens_focus_distance_label.setObjectName(
            u"camera_lens_focus_distance_label")

        self.camera_lens_focus_distance_layout.addWidget(
            self.camera_lens_focus_distance_label)

        self.camera_lens_focus_distance_spin_box = QDoubleSpinBox(
            self.layoutWidget)
        self.camera_lens_focus_distance_spin_box.setObjectName(
            u"camera_lens_focus_distance_spin_box")
        self.camera_lens_focus_distance_spin_box.setDecimals(2)
        self.camera_lens_focus_distance_spin_box.setMinimum(0.000000000000000)
        self.camera_lens_focus_distance_spin_box.setMaximum(1.000000000000000)
        self.camera_lens_focus_distance_spin_box.setSingleStep(
            0.010000000000000)
        self.camera_lens_focus_distance_spin_box.setValue(0.000000000000000)

        self.camera_lens_focus_distance_layout.addWidget(
            self.camera_lens_focus_distance_spin_box)

        self.camera_lens_layout.addLayout(
            self.camera_lens_focus_distance_layout)

        self.camera_lens_diameter_layout = QHBoxLayout()
        self.camera_lens_diameter_layout.setObjectName(
            u"camera_lens_diameter_layout")
        self.camera_lens_diameter_label = QLabel(self.layoutWidget)
        self.camera_lens_diameter_label.setObjectName(
            u"camera_lens_diameter_label")

        self.camera_lens_diameter_layout.addWidget(
            self.camera_lens_diameter_label)

        self.camera_lens_diameter_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_lens_diameter_spin_box.setObjectName(
            u"camera_lens_diameter_spin_box")
        self.camera_lens_diameter_spin_box.setDecimals(2)
        self.camera_lens_diameter_spin_box.setMinimum(0.000000000000000)
        self.camera_lens_diameter_spin_box.setMaximum(999.990000000000009)
        self.camera_lens_diameter_spin_box.setSingleStep(0.010000000000000)
        self.camera_lens_diameter_spin_box.setValue(0.000000000000000)

        self.camera_lens_diameter_layout.addWidget(
            self.camera_lens_diameter_spin_box)

        self.camera_lens_layout.addLayout(self.camera_lens_diameter_layout)

        self.camera_lens_length_layout = QHBoxLayout()
        self.camera_lens_length_layout.setObjectName(
            u"camera_lens_length_layout")
        self.camera_lens_length_label = QLabel(self.layoutWidget)
        self.camera_lens_length_label.setObjectName(u"camera_lens_length_label")

        self.camera_lens_length_layout.addWidget(self.camera_lens_length_label)

        self.camera_lens_length_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_lens_length_spin_box.setObjectName(
            u"camera_lens_length_spin_box")
        self.camera_lens_length_spin_box.setDecimals(2)
        self.camera_lens_length_spin_box.setMinimum(0.000000000000000)
        self.camera_lens_length_spin_box.setMaximum(999.990000000000009)
        self.camera_lens_length_spin_box.setSingleStep(0.010000000000000)
        self.camera_lens_length_spin_box.setValue(0.000000000000000)

        self.camera_lens_length_layout.addWidget(
            self.camera_lens_length_spin_box)

        self.camera_lens_layout.addLayout(self.camera_lens_length_layout)

        self.camera_layout.addLayout(self.camera_lens_layout)

        self.camera_image_sensor_layout = QVBoxLayout()
        self.camera_image_sensor_layout.setObjectName(
            u"camera_image_sensor_layout")
        self.camera_image_sensor_label = QLabel(self.layoutWidget)
        self.camera_image_sensor_label.setObjectName(
            u"camera_image_sensor_label")

        self.camera_image_sensor_layout.addWidget(
            self.camera_image_sensor_label)

        self.camera_image_sensor_width_layout = QHBoxLayout()
        self.camera_image_sensor_width_layout.setObjectName(
            u"camera_image_sensor_width_layout")
        self.camera_image_sensor_width_label = QLabel(self.layoutWidget)
        self.camera_image_sensor_width_label.setObjectName(
            u"camera_image_sensor_width_label")

        self.camera_image_sensor_width_layout.addWidget(
            self.camera_image_sensor_width_label)

        self.camera_image_sensor_width_spin_box = QDoubleSpinBox(
            self.layoutWidget)
        self.camera_image_sensor_width_spin_box.setObjectName(
            u"camera_image_sensor_width_spin_box")
        self.camera_image_sensor_width_spin_box.setDecimals(2)
        self.camera_image_sensor_width_spin_box.setMinimum(0.000000000000000)
        self.camera_image_sensor_width_spin_box.setMaximum(999.990000000000009)
        self.camera_image_sensor_width_spin_box.setSingleStep(0.010000000000000)
        self.camera_image_sensor_width_spin_box.setValue(0.000000000000000)

        self.camera_image_sensor_width_layout.addWidget(
            self.camera_image_sensor_width_spin_box)

        self.camera_image_sensor_layout.addLayout(
            self.camera_image_sensor_width_layout)

        self.camera_image_sensor_height_layout = QHBoxLayout()
        self.camera_image_sensor_height_layout.setObjectName(
            u"camera_image_sensor_height_layout")
        self.camera_image_sensor_height_label = QLabel(self.layoutWidget)
        self.camera_image_sensor_height_label.setObjectName(
            u"camera_image_sensor_height_label")

        self.camera_image_sensor_height_layout.addWidget(
            self.camera_image_sensor_height_label)

        self.camera_image_sensor_height_spin_box = QDoubleSpinBox(
            self.layoutWidget)
        self.camera_image_sensor_height_spin_box.setObjectName(
            u"camera_image_sensor_height_spin_box")
        self.camera_image_sensor_height_spin_box.setDecimals(2)
        self.camera_image_sensor_height_spin_box.setMinimum(0.000000000000000)
        self.camera_image_sensor_height_spin_box.setMaximum(999.990000000000009)
        self.camera_image_sensor_height_spin_box.setSingleStep(
            0.010000000000000)
        self.camera_image_sensor_height_spin_box.setValue(0.000000000000000)

        self.camera_image_sensor_height_layout.addWidget(
            self.camera_image_sensor_height_spin_box)

        self.camera_image_sensor_layout.addLayout(
            self.camera_image_sensor_height_layout)

        self.camera_image_sensor_pixel_size_layout = QHBoxLayout()
        self.camera_image_sensor_pixel_size_layout.setObjectName(
            u"camera_image_sensor_pixel_size_layout")
        self.camera_image_sensor_pixel_size_label = QLabel(self.layoutWidget)
        self.camera_image_sensor_pixel_size_label.setObjectName(
            u"camera_image_sensor_pixel_size_label")

        self.camera_image_sensor_pixel_size_layout.addWidget(
            self.camera_image_sensor_pixel_size_label)

        self.camera_image_sensor_pixel_size_spin_box = QDoubleSpinBox(
            self.layoutWidget)
        self.camera_image_sensor_pixel_size_spin_box.setObjectName(
            u"camera_image_sensor_pixel_size_spin_box")
        self.camera_image_sensor_pixel_size_spin_box.setDecimals(2)
        self.camera_image_sensor_pixel_size_spin_box.setMinimum(
            0.000000000000000)
        self.camera_image_sensor_pixel_size_spin_box.setMaximum(
            999.990000000000009)
        self.camera_image_sensor_pixel_size_spin_box.setSingleStep(
            0.010000000000000)
        self.camera_image_sensor_pixel_size_spin_box.setValue(0.000000000000000)

        self.camera_image_sensor_pixel_size_layout.addWidget(
            self.camera_image_sensor_pixel_size_spin_box)

        self.camera_image_sensor_layout.addLayout(
            self.camera_image_sensor_pixel_size_layout)

        self.camera_layout.addLayout(self.camera_image_sensor_layout)

        self.camera_coordinates_layout = QVBoxLayout()
        self.camera_coordinates_layout.setObjectName(
            u"camera_coordinates_layout")
        self.camera_coordinates_label = QLabel(self.layoutWidget)
        self.camera_coordinates_label.setObjectName(u"camera_coordinates_label")

        self.camera_coordinates_layout.addWidget(self.camera_coordinates_label)

        self.camera_coordinates_x_layout = QHBoxLayout()
        self.camera_coordinates_x_layout.setObjectName(
            u"camera_coordinates_x_layout")
        self.camera_coordinates_x_label = QLabel(self.layoutWidget)
        self.camera_coordinates_x_label.setObjectName(
            u"camera_coordinates_x_label")

        self.camera_coordinates_x_layout.addWidget(
            self.camera_coordinates_x_label)

        self.camera_coordinates_x_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_coordinates_x_spin_box.setObjectName(
            u"camera_coordinates_x_spin_box")
        self.camera_coordinates_x_spin_box.setDecimals(2)
        self.camera_coordinates_x_spin_box.setMinimum(-999.990000000000009)
        self.camera_coordinates_x_spin_box.setMaximum(999.990000000000009)
        self.camera_coordinates_x_spin_box.setSingleStep(0.010000000000000)
        self.camera_coordinates_x_spin_box.setValue(0.000000000000000)

        self.camera_coordinates_x_layout.addWidget(
            self.camera_coordinates_x_spin_box)

        self.camera_coordinates_layout.addLayout(
            self.camera_coordinates_x_layout)

        self.camera_coordinates_y_layout = QHBoxLayout()
        self.camera_coordinates_y_layout.setObjectName(
            u"camera_coordinates_y_layout")
        self.camera_coordinates_y_label = QLabel(self.layoutWidget)
        self.camera_coordinates_y_label.setObjectName(
            u"camera_coordinates_y_label")

        self.camera_coordinates_y_layout.addWidget(
            self.camera_coordinates_y_label)

        self.camera_coordinates_y_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_coordinates_y_spin_box.setObjectName(
            u"camera_coordinates_y_spin_box")
        self.camera_coordinates_y_spin_box.setDecimals(2)
        self.camera_coordinates_y_spin_box.setMinimum(-999.990000000000009)
        self.camera_coordinates_y_spin_box.setMaximum(999.990000000000009)
        self.camera_coordinates_y_spin_box.setSingleStep(0.010000000000000)
        self.camera_coordinates_y_spin_box.setValue(0.000000000000000)

        self.camera_coordinates_y_layout.addWidget(
            self.camera_coordinates_y_spin_box)

        self.camera_coordinates_layout.addLayout(
            self.camera_coordinates_y_layout)

        self.camera_coordinates_z_layout = QHBoxLayout()
        self.camera_coordinates_z_layout.setObjectName(
            u"camera_coordinates_z_layout")
        self.camera_coordinates_z_label = QLabel(self.layoutWidget)
        self.camera_coordinates_z_label.setObjectName(
            u"camera_coordinates_z_label")

        self.camera_coordinates_z_layout.addWidget(
            self.camera_coordinates_z_label)

        self.camera_coordinates_z_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_coordinates_z_spin_box.setObjectName(
            u"camera_coordinates_z_spin_box")
        self.camera_coordinates_z_spin_box.setDecimals(2)
        self.camera_coordinates_z_spin_box.setMinimum(-999.990000000000009)
        self.camera_coordinates_z_spin_box.setMaximum(999.990000000000009)
        self.camera_coordinates_z_spin_box.setSingleStep(0.010000000000000)
        self.camera_coordinates_z_spin_box.setValue(0.000000000000000)

        self.camera_coordinates_z_layout.addWidget(
            self.camera_coordinates_z_spin_box)

        self.camera_coordinates_layout.addLayout(
            self.camera_coordinates_z_layout)

        self.camera_layout.addLayout(self.camera_coordinates_layout)

        self.camera_axis_layout = QVBoxLayout()
        self.camera_axis_layout.setObjectName(u"camera_axis_layout")
        self.camera_axis_label = QLabel(self.layoutWidget)
        self.camera_axis_label.setObjectName(u"camera_axis_label")

        self.camera_axis_layout.addWidget(self.camera_axis_label)

        self.camera_axis_pitch_layout = QHBoxLayout()
        self.camera_axis_pitch_layout.setObjectName(u"camera_axis_pitch_layout")
        self.camera_axis_pitch_label = QLabel(self.layoutWidget)
        self.camera_axis_pitch_label.setObjectName(u"camera_axis_pitch_label")

        self.camera_axis_pitch_layout.addWidget(self.camera_axis_pitch_label)

        self.camera_axis_pitch_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_axis_pitch_spin_box.setObjectName(
            u"camera_axis_pitch_spin_box")
        self.camera_axis_pitch_spin_box.setDecimals(2)
        self.camera_axis_pitch_spin_box.setMinimum(-999.990000000000009)
        self.camera_axis_pitch_spin_box.setMaximum(999.990000000000009)
        self.camera_axis_pitch_spin_box.setSingleStep(0.010000000000000)
        self.camera_axis_pitch_spin_box.setValue(0.000000000000000)

        self.camera_axis_pitch_layout.addWidget(self.camera_axis_pitch_spin_box)

        self.camera_axis_layout.addLayout(self.camera_axis_pitch_layout)

        self.camera_axis_yaw_layout = QHBoxLayout()
        self.camera_axis_yaw_layout.setObjectName(u"camera_axis_yaw_layout")
        self.camera_axis_yaw_label = QLabel(self.layoutWidget)
        self.camera_axis_yaw_label.setObjectName(u"camera_axis_yaw_label")

        self.camera_axis_yaw_layout.addWidget(self.camera_axis_yaw_label)

        self.camera_axis_yaw_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_axis_yaw_spin_box.setObjectName(u"camera_axis_yaw_spin_box")
        self.camera_axis_yaw_spin_box.setDecimals(2)
        self.camera_axis_yaw_spin_box.setMinimum(-999.990000000000009)
        self.camera_axis_yaw_spin_box.setMaximum(999.990000000000009)
        self.camera_axis_yaw_spin_box.setSingleStep(0.010000000000000)
        self.camera_axis_yaw_spin_box.setValue(0.000000000000000)

        self.camera_axis_yaw_layout.addWidget(self.camera_axis_yaw_spin_box)

        self.camera_axis_layout.addLayout(self.camera_axis_yaw_layout)

        self.camera_axis_roll_layout = QHBoxLayout()
        self.camera_axis_roll_layout.setObjectName(u"camera_axis_roll_layout")
        self.camera_axis_roll_label = QLabel(self.layoutWidget)
        self.camera_axis_roll_label.setObjectName(u"camera_axis_roll_label")

        self.camera_axis_roll_layout.addWidget(self.camera_axis_roll_label)

        self.camera_axis_roll_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.camera_axis_roll_spin_box.setObjectName(
            u"camera_axis_roll_spin_box")
        self.camera_axis_roll_spin_box.setDecimals(2)
        self.camera_axis_roll_spin_box.setMinimum(-999.990000000000009)
        self.camera_axis_roll_spin_box.setMaximum(999.990000000000009)
        self.camera_axis_roll_spin_box.setSingleStep(0.010000000000000)
        self.camera_axis_roll_spin_box.setValue(0.000000000000000)

        self.camera_axis_roll_layout.addWidget(self.camera_axis_roll_spin_box)

        self.camera_axis_layout.addLayout(self.camera_axis_roll_layout)

        self.camera_error_label = QLabel(self.layoutWidget)
        self.camera_error_label.setObjectName(u"camera_error_label")

        self.camera_axis_layout.addWidget(self.camera_error_label)

        self.camera_layout.addLayout(self.camera_axis_layout)

        self.camera_save_layout = QHBoxLayout()
        self.camera_save_layout.setObjectName(u"camera_save_layout")
        self.camera_create_button = QPushButton(self.layoutWidget)
        self.camera_create_button.setObjectName(u"camera_create_button")
        self.camera_create_button.setAutoDefault(False)

        self.camera_save_layout.addWidget(self.camera_create_button)

        self.camera_close_button = QPushButton(self.layoutWidget)
        self.camera_close_button.setObjectName(u"camera_close_button")
        self.camera_close_button.setAutoDefault(False)

        self.camera_save_layout.addWidget(self.camera_close_button)

        self.camera_layout.addLayout(self.camera_save_layout)

        self.retranslateUi(camera_dialog)

        QMetaObject.connectSlotsByName(camera_dialog)

    # setupUi

    def retranslateUi(self, camera_dialog):
        camera_dialog.setWindowTitle(
            QCoreApplication.translate("camera_dialog", u"Dialog", None))
        self.camera_label.setText(
            QCoreApplication.translate("camera_dialog",
                                       u"\u041a\u0430\u043c\u0435\u0440\u0430",
                                       None))
        self.camera_size_label.setText(
            QCoreApplication.translate(
                "camera_dialog", u"\u0420\u0430\u0437\u043c\u0435\u0440\u044b",
                None))
        self.camera_size_length_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0414\u043b\u0438\u043d\u0430(\u043c\u043c):", None))
        self.camera_size_width_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0428\u0438\u0440\u0438\u043d\u0430(\u043c\u043c):", None))
        self.camera_size_height_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0412\u044b\u0441\u043e\u0442\u0430(\u043c\u043c):", None))
        self.camera_lens_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u041e\u0431\u044a\u0435\u043a\u0442\u0438\u0432", None))
        self.camera_lens_focal_length_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0424\u043e\u043a\u0443\u0441\u043d\u043e\u0435 \u0440\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435(\u043c\u043c):",
                None))
        self.camera_lens_f_number_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0414\u0438\u0430\u0444\u0440\u0430\u0433\u043c\u0435\u043d\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e:",
                None))
        self.camera_lens_focus_distance_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0444\u043e\u043a\u0443\u0441\u0438\u0440\u043e\u0432\u043a\u0438(H):",
                None))
        self.camera_lens_diameter_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0414\u0438\u0430\u043c\u0435\u0442\u0440(\u043c\u043c):",
                None))
        self.camera_lens_length_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0414\u043b\u0438\u043d\u0430(\u043c\u043c):", None))
        self.camera_image_sensor_label.setText(
            QCoreApplication.translate(
                "camera_dialog", u"\u041c\u0430\u0442\u0440\u0438\u0446\u0430",
                None))
        self.camera_image_sensor_width_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0428\u0438\u0440\u0438\u043d\u0430(\u043c\u043c):", None))
        self.camera_image_sensor_height_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0412\u044b\u0441\u043e\u0442\u0430(\u043c\u043c):", None))
        self.camera_image_sensor_pixel_size_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0420\u0430\u0437\u043c\u0435\u0440 \u043f\u0438\u043a\u0441\u0435\u043b\u0435\u0439(\u043c\u043a\u043c):",
                None))
        self.camera_coordinates_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b",
                None))
        self.camera_coordinates_x_label.setText(
            QCoreApplication.translate("camera_dialog", u"x(\u043c\u043c):",
                                       None))
        self.camera_coordinates_y_label.setText(
            QCoreApplication.translate("camera_dialog", u"y(\u043c\u043c):",
                                       None))
        self.camera_coordinates_z_label.setText(
            QCoreApplication.translate("camera_dialog", u"z(\u043c\u043c):",
                                       None))
        self.camera_axis_label.setText(
            QCoreApplication.translate("camera_dialog", u"\u041e\u0441\u0438",
                                       None))
        self.camera_axis_pitch_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0422\u0430\u043d\u0433\u0430\u0436(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.camera_axis_yaw_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u0420\u044b\u0441\u043a\u0430\u043d\u044c\u0435(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.camera_axis_roll_label.setText(
            QCoreApplication.translate(
                "camera_dialog",
                u"\u041a\u0440\u0435\u043d(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.camera_error_label.setText("")
        self.camera_create_button.setText(
            QCoreApplication.translate(
                "camera_dialog", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c",
                None))
        self.camera_close_button.setText(
            QCoreApplication.translate("camera_dialog",
                                       u"\u041e\u0442\u043c\u0435\u043d\u0430",
                                       None))

    # retranslateUi
