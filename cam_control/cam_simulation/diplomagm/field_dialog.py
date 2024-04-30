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


class Ui_field_dialog(object):

    def setupUi(self, field_dialog):
        if not field_dialog.objectName():
            field_dialog.setObjectName(u"field_dialog")
        field_dialog.resize(400, 372)
        self.layoutWidget = QWidget(field_dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 371, 331))
        self.field_layout = QVBoxLayout(self.layoutWidget)
        self.field_layout.setObjectName(u"field_layout")
        self.field_layout.setContentsMargins(0, 0, 0, 0)
        self.field_label = QLabel(self.layoutWidget)
        self.field_label.setObjectName(u"field_label")

        self.field_layout.addWidget(self.field_label)

        self.field_size_layout = QVBoxLayout()
        self.field_size_layout.setObjectName(u"field_size_layout")
        self.field_size_label = QLabel(self.layoutWidget)
        self.field_size_label.setObjectName(u"field_size_label")

        self.field_size_layout.addWidget(self.field_size_label)

        self.field_size_length_layout = QHBoxLayout()
        self.field_size_length_layout.setObjectName(u"field_size_length_layout")
        self.field_size_length_label = QLabel(self.layoutWidget)
        self.field_size_length_label.setObjectName(u"field_size_length_label")

        self.field_size_length_layout.addWidget(self.field_size_length_label)

        self.field_size_length_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.field_size_length_spin_box.setObjectName(
            u"field_size_length_spin_box")
        self.field_size_length_spin_box.setDecimals(2)
        self.field_size_length_spin_box.setMinimum(0.000000000000000)
        self.field_size_length_spin_box.setMaximum(999.990000000000009)
        self.field_size_length_spin_box.setSingleStep(0.010000000000000)
        self.field_size_length_spin_box.setValue(0.000000000000000)

        self.field_size_length_layout.addWidget(self.field_size_length_spin_box)

        self.field_size_layout.addLayout(self.field_size_length_layout)

        self.field_size_width_layout = QHBoxLayout()
        self.field_size_width_layout.setObjectName(u"field_size_width_layout")
        self.field_size_width_label = QLabel(self.layoutWidget)
        self.field_size_width_label.setObjectName(u"field_size_width_label")

        self.field_size_width_layout.addWidget(self.field_size_width_label)

        self.field_size_width_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.field_size_width_spin_box.setObjectName(
            u"field_size_width_spin_box")
        self.field_size_width_spin_box.setDecimals(2)
        self.field_size_width_spin_box.setMinimum(0.000000000000000)
        self.field_size_width_spin_box.setMaximum(999.990000000000009)
        self.field_size_width_spin_box.setSingleStep(0.010000000000000)
        self.field_size_width_spin_box.setValue(0.000000000000000)

        self.field_size_width_layout.addWidget(self.field_size_width_spin_box)

        self.field_size_layout.addLayout(self.field_size_width_layout)

        self.field_layout.addLayout(self.field_size_layout)

        self.field_coordinates_layout = QVBoxLayout()
        self.field_coordinates_layout.setObjectName(u"field_coordinates_layout")
        self.field_coordinates_label = QLabel(self.layoutWidget)
        self.field_coordinates_label.setObjectName(u"field_coordinates_label")

        self.field_coordinates_layout.addWidget(self.field_coordinates_label)

        self.field_coordinates_x_layout = QHBoxLayout()
        self.field_coordinates_x_layout.setObjectName(
            u"field_coordinates_x_layout")
        self.field_coordinates_x_label = QLabel(self.layoutWidget)
        self.field_coordinates_x_label.setObjectName(
            u"field_coordinates_x_label")

        self.field_coordinates_x_layout.addWidget(
            self.field_coordinates_x_label)

        self.field_coordinates_x_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.field_coordinates_x_spin_box.setObjectName(
            u"field_coordinates_x_spin_box")
        self.field_coordinates_x_spin_box.setDecimals(2)
        self.field_coordinates_x_spin_box.setMinimum(-999.990000000000009)
        self.field_coordinates_x_spin_box.setMaximum(999.990000000000009)
        self.field_coordinates_x_spin_box.setSingleStep(0.010000000000000)
        self.field_coordinates_x_spin_box.setValue(0.000000000000000)

        self.field_coordinates_x_layout.addWidget(
            self.field_coordinates_x_spin_box)

        self.field_coordinates_layout.addLayout(self.field_coordinates_x_layout)

        self.field_coordinates_y_layout = QHBoxLayout()
        self.field_coordinates_y_layout.setObjectName(
            u"field_coordinates_y_layout")
        self.field_coordinates_y_label = QLabel(self.layoutWidget)
        self.field_coordinates_y_label.setObjectName(
            u"field_coordinates_y_label")

        self.field_coordinates_y_layout.addWidget(
            self.field_coordinates_y_label)

        self.field_coordinates_y_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.field_coordinates_y_spin_box.setObjectName(
            u"field_coordinates_y_spin_box")
        self.field_coordinates_y_spin_box.setDecimals(2)
        self.field_coordinates_y_spin_box.setMinimum(-999.990000000000009)
        self.field_coordinates_y_spin_box.setMaximum(999.990000000000009)
        self.field_coordinates_y_spin_box.setSingleStep(0.010000000000000)
        self.field_coordinates_y_spin_box.setValue(0.000000000000000)

        self.field_coordinates_y_layout.addWidget(
            self.field_coordinates_y_spin_box)

        self.field_coordinates_layout.addLayout(self.field_coordinates_y_layout)

        self.field_layout.addLayout(self.field_coordinates_layout)

        self.field_grandstand_layout = QHBoxLayout()
        self.field_grandstand_layout.setObjectName(u"field_grandstand_layout")
        self.field_grandstand_label = QLabel(self.layoutWidget)
        self.field_grandstand_label.setObjectName(u"field_grandstand_label")

        self.field_grandstand_layout.addWidget(self.field_grandstand_label)

        self.field_grandstand_spin_box = QDoubleSpinBox(self.layoutWidget)
        self.field_grandstand_spin_box.setObjectName(
            u"field_grandstand_spin_box")
        self.field_grandstand_spin_box.setDecimals(2)
        self.field_grandstand_spin_box.setMinimum(0.000000000000000)
        self.field_grandstand_spin_box.setMaximum(999.990000000000009)
        self.field_grandstand_spin_box.setSingleStep(0.010000000000000)
        self.field_grandstand_spin_box.setValue(0.000000000000000)

        self.field_grandstand_layout.addWidget(self.field_grandstand_spin_box)

        self.field_layout.addLayout(self.field_grandstand_layout)

        self.field_error_label = QLabel(self.layoutWidget)
        self.field_error_label.setObjectName(u"field_error_label")

        self.field_layout.addWidget(self.field_error_label)

        self.field_save_layout = QHBoxLayout()
        self.field_save_layout.setObjectName(u"field_save_layout")
        self.field_save_button = QPushButton(self.layoutWidget)
        self.field_save_button.setObjectName(u"field_save_button")
        self.field_save_button.setAutoDefault(False)

        self.field_save_layout.addWidget(self.field_save_button)

        self.field_save_as_button = QPushButton(self.layoutWidget)
        self.field_save_as_button.setObjectName(u"field_save_as_button")
        self.field_save_as_button.setAutoDefault(False)

        self.field_save_layout.addWidget(self.field_save_as_button)

        self.field_close_button = QPushButton(self.layoutWidget)
        self.field_close_button.setObjectName(u"field_close_button")
        self.field_close_button.setAutoDefault(False)

        self.field_save_layout.addWidget(self.field_close_button)

        self.field_layout.addLayout(self.field_save_layout)

        self.retranslateUi(field_dialog)

        QMetaObject.connectSlotsByName(field_dialog)

    # setupUi

    def retranslateUi(self, field_dialog):
        field_dialog.setWindowTitle(
            QCoreApplication.translate("field_dialog", u"Dialog", None))
        self.field_label.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u0424\u0443\u0442\u0431\u043e\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435",
                None))
        self.field_size_label.setText(
            QCoreApplication.translate(
                "field_dialog", u"\u0420\u0430\u0437\u043c\u0435\u0440\u044b",
                None))
        self.field_size_length_label.setText(
            QCoreApplication.translate(
                "field_dialog", u"\u0414\u043b\u0438\u043d\u0430(\u043c):",
                None))
        self.field_size_width_label.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u0428\u0438\u0440\u0438\u043d\u0430(\u043c):", None))
        self.field_coordinates_label.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b",
                None))
        self.field_coordinates_x_label.setText(
            QCoreApplication.translate("field_dialog", u"x(\u043c):", None))
        self.field_coordinates_y_label.setText(
            QCoreApplication.translate("field_dialog", u"y(\u043c):", None))
        self.field_grandstand_label.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u0428\u0438\u0440\u0438\u043d\u0430 \u0442\u0440\u0438\u0431\u0443\u043d(\u043c):",
                None))
        self.field_error_label.setText("")
        self.field_save_button.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
                None))
        self.field_save_as_button.setText(
            QCoreApplication.translate(
                "field_dialog",
                u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a...",
                None))
        self.field_close_button.setText(
            QCoreApplication.translate("field_dialog",
                                       u"\u041e\u0442\u043c\u0435\u043d\u0430",
                                       None))

    # retranslateUi
