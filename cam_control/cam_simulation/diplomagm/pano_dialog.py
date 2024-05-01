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


class Ui_pano_dialog(object):

    def setupUi(self, pano_dialog):
        if not pano_dialog.objectName():
            pano_dialog.setObjectName(u"pano_dialog")
        pano_dialog.resize(400, 500)
        self.layoutWidget_10 = QWidget(pano_dialog)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(20, 20, 361, 469))
        self.pano_layout = QVBoxLayout(self.layoutWidget_10)
        self.pano_layout.setObjectName(u"pano_layout")
        self.pano_layout.setContentsMargins(0, 0, 0, 0)
        self.pano_label = QLabel(self.layoutWidget_10)
        self.pano_label.setObjectName(u"pano_label")

        self.pano_layout.addWidget(self.pano_label)

        self.pano_size_layout = QVBoxLayout()
        self.pano_size_layout.setObjectName(u"pano_size_layout")
        self.label_2 = QLabel(self.layoutWidget_10)
        self.label_2.setObjectName(u"label_2")

        self.pano_size_layout.addWidget(self.label_2)

        self.pano_size_length_layout = QHBoxLayout()
        self.pano_size_length_layout.setObjectName(u"pano_size_length_layout")
        self.pano_size_length_label = QLabel(self.layoutWidget_10)
        self.pano_size_length_label.setObjectName(u"pano_size_length_label")

        self.pano_size_length_layout.addWidget(self.pano_size_length_label)

        self.pano_size_length_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_size_length_spin_box.setObjectName(
            u"pano_size_length_spin_box")
        self.pano_size_length_spin_box.setReadOnly(False)
        self.pano_size_length_spin_box.setDecimals(2)
        self.pano_size_length_spin_box.setMinimum(0.000000000000000)
        self.pano_size_length_spin_box.setMaximum(999.990000000000009)
        self.pano_size_length_spin_box.setSingleStep(0.010000000000000)
        self.pano_size_length_spin_box.setValue(0.000000000000000)

        self.pano_size_length_layout.addWidget(self.pano_size_length_spin_box)

        self.pano_size_layout.addLayout(self.pano_size_length_layout)

        self.pano_size_width_layout = QHBoxLayout()
        self.pano_size_width_layout.setObjectName(u"pano_size_width_layout")
        self.pano_size_width_label = QLabel(self.layoutWidget_10)
        self.pano_size_width_label.setObjectName(u"pano_size_width_label")

        self.pano_size_width_layout.addWidget(self.pano_size_width_label)

        self.pano_size_width_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_size_width_spin_box.setObjectName(u"pano_size_width_spin_box")
        self.pano_size_width_spin_box.setReadOnly(False)
        self.pano_size_width_spin_box.setDecimals(2)
        self.pano_size_width_spin_box.setMinimum(0.000000000000000)
        self.pano_size_width_spin_box.setMaximum(999.990000000000009)
        self.pano_size_width_spin_box.setSingleStep(0.010000000000000)
        self.pano_size_width_spin_box.setValue(0.000000000000000)

        self.pano_size_width_layout.addWidget(self.pano_size_width_spin_box)

        self.pano_size_layout.addLayout(self.pano_size_width_layout)

        self.pano_size_height_layout = QHBoxLayout()
        self.pano_size_height_layout.setObjectName(u"pano_size_height_layout")
        self.pano_size_height_label = QLabel(self.layoutWidget_10)
        self.pano_size_height_label.setObjectName(u"pano_size_height_label")

        self.pano_size_height_layout.addWidget(self.pano_size_height_label)

        self.pano_size_height_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_size_height_spin_box.setObjectName(
            u"pano_size_height_spin_box")
        self.pano_size_height_spin_box.setReadOnly(False)
        self.pano_size_height_spin_box.setDecimals(2)
        self.pano_size_height_spin_box.setMinimum(0.000000000000000)
        self.pano_size_height_spin_box.setMaximum(999.990000000000009)
        self.pano_size_height_spin_box.setSingleStep(0.010000000000000)
        self.pano_size_height_spin_box.setValue(0.000000000000000)

        self.pano_size_height_layout.addWidget(self.pano_size_height_spin_box)

        self.pano_size_layout.addLayout(self.pano_size_height_layout)

        self.pano_layout.addLayout(self.pano_size_layout)

        self.pano_coordinates_layout = QVBoxLayout()
        self.pano_coordinates_layout.setObjectName(u"pano_coordinates_layout")
        self.pano_coordinates_label = QLabel(self.layoutWidget_10)
        self.pano_coordinates_label.setObjectName(u"pano_coordinates_label")

        self.pano_coordinates_layout.addWidget(self.pano_coordinates_label)

        self.pano_coordinates_x_layout = QHBoxLayout()
        self.pano_coordinates_x_layout.setObjectName(
            u"pano_coordinates_x_layout")
        self.pano_coordinates_x_label = QLabel(self.layoutWidget_10)
        self.pano_coordinates_x_label.setObjectName(u"pano_coordinates_x_label")

        self.pano_coordinates_x_layout.addWidget(self.pano_coordinates_x_label)

        self.pano_coordinates_x_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_coordinates_x_spin_box.setObjectName(
            u"pano_coordinates_x_spin_box")
        self.pano_coordinates_x_spin_box.setDecimals(2)
        self.pano_coordinates_x_spin_box.setMinimum(-999.990000000000009)
        self.pano_coordinates_x_spin_box.setMaximum(999.990000000000009)
        self.pano_coordinates_x_spin_box.setSingleStep(0.010000000000000)
        self.pano_coordinates_x_spin_box.setValue(0.000000000000000)

        self.pano_coordinates_x_layout.addWidget(
            self.pano_coordinates_x_spin_box)

        self.pano_coordinates_layout.addLayout(self.pano_coordinates_x_layout)

        self.pano_coordinates_y_layout = QHBoxLayout()
        self.pano_coordinates_y_layout.setObjectName(
            u"pano_coordinates_y_layout")
        self.pano_coordinates_y_label = QLabel(self.layoutWidget_10)
        self.pano_coordinates_y_label.setObjectName(u"pano_coordinates_y_label")

        self.pano_coordinates_y_layout.addWidget(self.pano_coordinates_y_label)

        self.pano_coordinates_y_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_coordinates_y_spin_box.setObjectName(
            u"pano_coordinates_y_spin_box")
        self.pano_coordinates_y_spin_box.setDecimals(2)
        self.pano_coordinates_y_spin_box.setMinimum(-999.990000000000009)
        self.pano_coordinates_y_spin_box.setMaximum(999.990000000000009)
        self.pano_coordinates_y_spin_box.setSingleStep(0.010000000000000)
        self.pano_coordinates_y_spin_box.setValue(0.000000000000000)

        self.pano_coordinates_y_layout.addWidget(
            self.pano_coordinates_y_spin_box)

        self.pano_coordinates_layout.addLayout(self.pano_coordinates_y_layout)

        self.pano_coordinates_z_layout = QHBoxLayout()
        self.pano_coordinates_z_layout.setObjectName(
            u"pano_coordinates_z_layout")
        self.pano_coordinates_z_label = QLabel(self.layoutWidget_10)
        self.pano_coordinates_z_label.setObjectName(u"pano_coordinates_z_label")

        self.pano_coordinates_z_layout.addWidget(self.pano_coordinates_z_label)

        self.pano_coordinates_z_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_coordinates_z_spin_box.setObjectName(
            u"pano_coordinates_z_spin_box")
        self.pano_coordinates_z_spin_box.setDecimals(2)
        self.pano_coordinates_z_spin_box.setMinimum(-999.990000000000009)
        self.pano_coordinates_z_spin_box.setMaximum(999.990000000000009)
        self.pano_coordinates_z_spin_box.setSingleStep(0.010000000000000)
        self.pano_coordinates_z_spin_box.setValue(0.000000000000000)

        self.pano_coordinates_z_layout.addWidget(
            self.pano_coordinates_z_spin_box)

        self.pano_coordinates_layout.addLayout(self.pano_coordinates_z_layout)

        self.pano_layout.addLayout(self.pano_coordinates_layout)

        self.pano_axis_layout = QVBoxLayout()
        self.pano_axis_layout.setObjectName(u"pano_axis_layout")
        self.pano_axis_label = QLabel(self.layoutWidget_10)
        self.pano_axis_label.setObjectName(u"pano_axis_label")

        self.pano_axis_layout.addWidget(self.pano_axis_label)

        self.pano_axis_pitch_layout = QHBoxLayout()
        self.pano_axis_pitch_layout.setObjectName(u"pano_axis_pitch_layout")
        self.pano_axis_pitch_label = QLabel(self.layoutWidget_10)
        self.pano_axis_pitch_label.setObjectName(u"pano_axis_pitch_label")

        self.pano_axis_pitch_layout.addWidget(self.pano_axis_pitch_label)

        self.pano_axis_pitch_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_axis_pitch_spin_box.setObjectName(u"pano_axis_pitch_spin_box")
        self.pano_axis_pitch_spin_box.setDecimals(2)
        self.pano_axis_pitch_spin_box.setMinimum(-999.990000000000009)
        self.pano_axis_pitch_spin_box.setMaximum(999.990000000000009)
        self.pano_axis_pitch_spin_box.setSingleStep(0.010000000000000)
        self.pano_axis_pitch_spin_box.setValue(0.000000000000000)

        self.pano_axis_pitch_layout.addWidget(self.pano_axis_pitch_spin_box)

        self.pano_axis_layout.addLayout(self.pano_axis_pitch_layout)

        self.pano_axis_yaw_layout = QHBoxLayout()
        self.pano_axis_yaw_layout.setObjectName(u"pano_axis_yaw_layout")
        self.pano_axis_yaw_label = QLabel(self.layoutWidget_10)
        self.pano_axis_yaw_label.setObjectName(u"pano_axis_yaw_label")

        self.pano_axis_yaw_layout.addWidget(self.pano_axis_yaw_label)

        self.pano_axis_yaw_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_axis_yaw_spin_box.setObjectName(u"pano_axis_yaw_spin_box")
        self.pano_axis_yaw_spin_box.setDecimals(2)
        self.pano_axis_yaw_spin_box.setMinimum(-999.990000000000009)
        self.pano_axis_yaw_spin_box.setMaximum(999.990000000000009)
        self.pano_axis_yaw_spin_box.setSingleStep(0.010000000000000)
        self.pano_axis_yaw_spin_box.setValue(0.000000000000000)

        self.pano_axis_yaw_layout.addWidget(self.pano_axis_yaw_spin_box)

        self.pano_axis_layout.addLayout(self.pano_axis_yaw_layout)

        self.pano_axis_roll_layout = QHBoxLayout()
        self.pano_axis_roll_layout.setObjectName(u"pano_axis_roll_layout")
        self.pano_axis_roll_label = QLabel(self.layoutWidget_10)
        self.pano_axis_roll_label.setObjectName(u"pano_axis_roll_label")

        self.pano_axis_roll_layout.addWidget(self.pano_axis_roll_label)

        self.pano_axis_roll_spin_box = QDoubleSpinBox(self.layoutWidget_10)
        self.pano_axis_roll_spin_box.setObjectName(u"pano_axis_roll_spin_box")
        self.pano_axis_roll_spin_box.setDecimals(2)
        self.pano_axis_roll_spin_box.setMinimum(-999.990000000000009)
        self.pano_axis_roll_spin_box.setMaximum(999.990000000000009)
        self.pano_axis_roll_spin_box.setSingleStep(0.010000000000000)
        self.pano_axis_roll_spin_box.setValue(0.000000000000000)

        self.pano_axis_roll_layout.addWidget(self.pano_axis_roll_spin_box)

        self.pano_axis_layout.addLayout(self.pano_axis_roll_layout)

        self.pano_layout.addLayout(self.pano_axis_layout)

        self.pano_error_label = QLabel(self.layoutWidget_10)
        self.pano_error_label.setObjectName(u"pano_error_label")

        self.pano_layout.addWidget(self.pano_error_label)

        self.pano_save_layout = QHBoxLayout()
        self.pano_save_layout.setObjectName(u"pano_save_layout")
        self.pano_create_button = QPushButton(self.layoutWidget_10)
        self.pano_create_button.setObjectName(u"pano_create_button")
        self.pano_create_button.setAutoDefault(False)

        self.pano_save_layout.addWidget(self.pano_create_button)

        self.pano_close_button = QPushButton(self.layoutWidget_10)
        self.pano_close_button.setObjectName(u"pano_close_button")
        self.pano_close_button.setAutoDefault(False)

        self.pano_save_layout.addWidget(self.pano_close_button)

        self.pano_layout.addLayout(self.pano_save_layout)

        self.retranslateUi(pano_dialog)

        QMetaObject.connectSlotsByName(pano_dialog)

    # setupUi

    def retranslateUi(self, pano_dialog):
        pano_dialog.setWindowTitle(
            QCoreApplication.translate("pano_dialog", u"Dialog", None))
        self.pano_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u041f\u0430\u043d\u043e\u0440\u0430\u043c\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430",
                None))
        self.label_2.setText(
            QCoreApplication.translate(
                "pano_dialog", u"\u0420\u0430\u0437\u043c\u0435\u0440\u044b",
                None))
        self.pano_size_length_label.setText(
            QCoreApplication.translate(
                "pano_dialog", u"\u0414\u043b\u0438\u043d\u0430(\u043c\u043c):",
                None))
        self.pano_size_width_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u0428\u0438\u0440\u0438\u043d\u0430(\u043c\u043c):", None))
        self.pano_size_height_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u0412\u044b\u0441\u043e\u0442\u0430(\u043c\u043c):", None))
        self.pano_coordinates_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b",
                None))
        self.pano_coordinates_x_label.setText(
            QCoreApplication.translate("pano_dialog", u"x(\u043c):", None))
        self.pano_coordinates_y_label.setText(
            QCoreApplication.translate("pano_dialog", u"y(\u043c):", None))
        self.pano_coordinates_z_label.setText(
            QCoreApplication.translate("pano_dialog", u"z(\u043c):", None))
        self.pano_axis_label.setText(
            QCoreApplication.translate("pano_dialog", u"\u041e\u0441\u0438",
                                       None))
        self.pano_axis_pitch_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u0422\u0430\u043d\u0433\u0430\u0436(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.pano_axis_yaw_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u0420\u044b\u0441\u043a\u0430\u043d\u044c\u0435(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.pano_axis_roll_label.setText(
            QCoreApplication.translate(
                "pano_dialog",
                u"\u041a\u0440\u0435\u043d(\u0433\u0440\u0430\u0434\u0443\u0441\u044b):",
                None))
        self.pano_error_label.setText("")
        self.pano_create_button.setText(
            QCoreApplication.translate(
                "pano_dialog", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c",
                None))
        self.pano_close_button.setText(
            QCoreApplication.translate("pano_dialog",
                                       u"\u041e\u0442\u043c\u0435\u043d\u0430",
                                       None))

    # retranslateUi
