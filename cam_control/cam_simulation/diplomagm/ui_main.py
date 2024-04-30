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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QSizePolicy, QTreeView, QVBoxLayout,
                               QWidget)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(790, 492)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.left_layout = QVBoxLayout()
        self.left_layout.setObjectName(u"left_layout")
        self.pano_list_layout = QVBoxLayout()
        self.pano_list_layout.setObjectName(u"pano_list_layout")
        self.pano_list_label = QLabel(self.centralwidget)
        self.pano_list_label.setObjectName(u"pano_list_label")

        self.pano_list_layout.addWidget(self.pano_list_label)

        self.pano_list_file_line = QLineEdit(self.centralwidget)
        self.pano_list_file_line.setObjectName(u"pano_list_file_line")
        self.pano_list_file_line.setReadOnly(True)

        self.pano_list_layout.addWidget(self.pano_list_file_line)

        self.pano_list_create_layout = QHBoxLayout()
        self.pano_list_create_layout.setObjectName(u"pano_list_create_layout")
        self.pano_list_create_button = QPushButton(self.centralwidget)
        self.pano_list_create_button.setObjectName(u"pano_list_create_button")

        self.pano_list_create_layout.addWidget(self.pano_list_create_button)

        self.pano_list_load_button = QPushButton(self.centralwidget)
        self.pano_list_load_button.setObjectName(u"pano_list_load_button")

        self.pano_list_create_layout.addWidget(self.pano_list_load_button)

        self.pano_list_clear_button = QPushButton(self.centralwidget)
        self.pano_list_clear_button.setObjectName(u"pano_list_clear_button")

        self.pano_list_create_layout.addWidget(self.pano_list_clear_button)

        self.pano_list_layout.addLayout(self.pano_list_create_layout)

        self.pano_list_tree = QTreeView(self.centralwidget)
        self.pano_list_tree.setObjectName(u"pano_list_tree")

        self.pano_list_layout.addWidget(self.pano_list_tree)

        self.left_layout.addLayout(self.pano_list_layout)

        self.pano_system_layout = QVBoxLayout()
        self.pano_system_layout.setObjectName(u"pano_system_layout")
        self.pano_layout = QVBoxLayout()
        self.pano_layout.setObjectName(u"pano_layout")
        self.pano_label = QLabel(self.centralwidget)
        self.pano_label.setObjectName(u"pano_label")

        self.pano_layout.addWidget(self.pano_label)

        self.pano_combo_box = QComboBox(self.centralwidget)
        self.pano_combo_box.setObjectName(u"pano_combo_box")

        self.pano_layout.addWidget(self.pano_combo_box)

        self.pano_create_layout = QHBoxLayout()
        self.pano_create_layout.setObjectName(u"pano_create_layout")
        self.pano_add_button = QPushButton(self.centralwidget)
        self.pano_add_button.setObjectName(u"pano_add_button")

        self.pano_create_layout.addWidget(self.pano_add_button)

        self.pano_change_button = QPushButton(self.centralwidget)
        self.pano_change_button.setObjectName(u"pano_change_button")

        self.pano_create_layout.addWidget(self.pano_change_button)

        self.pano_remove_button = QPushButton(self.centralwidget)
        self.pano_remove_button.setObjectName(u"pano_remove_button")

        self.pano_create_layout.addWidget(self.pano_remove_button)

        self.pano_layout.addLayout(self.pano_create_layout)

        self.pano_system_layout.addLayout(self.pano_layout)

        self.camera_layout = QVBoxLayout()
        self.camera_layout.setObjectName(u"camera_layout")
        self.camera_label = QLabel(self.centralwidget)
        self.camera_label.setObjectName(u"camera_label")
        self.camera_label.setMinimumSize(QSize(369, 0))
        self.camera_label.setMaximumSize(QSize(369, 30))

        self.camera_layout.addWidget(self.camera_label)

        self.camera_combo_box = QComboBox(self.centralwidget)
        self.camera_combo_box.setObjectName(u"camera_combo_box")

        self.camera_layout.addWidget(self.camera_combo_box)

        self.camera_create_layout = QHBoxLayout()
        self.camera_create_layout.setObjectName(u"camera_create_layout")
        self.camera_add_button = QPushButton(self.centralwidget)
        self.camera_add_button.setObjectName(u"camera_add_button")

        self.camera_create_layout.addWidget(self.camera_add_button)

        self.camera_change_button = QPushButton(self.centralwidget)
        self.camera_change_button.setObjectName(u"camera_change_button")

        self.camera_create_layout.addWidget(self.camera_change_button)

        self.camera_remove_button = QPushButton(self.centralwidget)
        self.camera_remove_button.setObjectName(u"camera_remove_button")

        self.camera_create_layout.addWidget(self.camera_remove_button)

        self.camera_layout.addLayout(self.camera_create_layout)

        self.pano_system_layout.addLayout(self.camera_layout)

        self.left_layout.addLayout(self.pano_system_layout)

        self.main_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setObjectName(u"right_layout")
        self.field_layout = QVBoxLayout()
        self.field_layout.setObjectName(u"field_layout")
        self.panoramic_system_layout = QVBoxLayout()
        self.panoramic_system_layout.setObjectName(u"panoramic_system_layout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.panoramic_system_layout.addWidget(self.label)

        self.panoramic_system_save_layout = QHBoxLayout()
        self.panoramic_system_save_layout.setObjectName(
            u"panoramic_system_save_layout")
        self.pano_list_save_button = QPushButton(self.centralwidget)
        self.pano_list_save_button.setObjectName(u"pano_list_save_button")

        self.panoramic_system_save_layout.addWidget(self.pano_list_save_button)

        self.pano_list_save_as_button = QPushButton(self.centralwidget)
        self.pano_list_save_as_button.setObjectName(u"pano_list_save_as_button")

        self.panoramic_system_save_layout.addWidget(
            self.pano_list_save_as_button)

        self.panoramic_system_layout.addLayout(
            self.panoramic_system_save_layout)

        self.field_layout.addLayout(self.panoramic_system_layout)

        self.field_label = QLabel(self.centralwidget)
        self.field_label.setObjectName(u"field_label")

        self.field_layout.addWidget(self.field_label)

        self.field_file_line = QLineEdit(self.centralwidget)
        self.field_file_line.setObjectName(u"field_file_line")
        self.field_file_line.setReadOnly(True)

        self.field_layout.addWidget(self.field_file_line)

        self.field_create_layout = QHBoxLayout()
        self.field_create_layout.setObjectName(u"field_create_layout")
        self.field_create_button = QPushButton(self.centralwidget)
        self.field_create_button.setObjectName(u"field_create_button")

        self.field_create_layout.addWidget(self.field_create_button)

        self.field_load_button = QPushButton(self.centralwidget)
        self.field_load_button.setObjectName(u"field_load_button")

        self.field_create_layout.addWidget(self.field_load_button)

        self.field_layout.addLayout(self.field_create_layout)

        self.right_layout.addLayout(self.field_layout)

        self.empty_label = QLabel(self.centralwidget)
        self.empty_label.setObjectName(u"empty_label")

        self.right_layout.addWidget(self.empty_label)

        self.create_model = QVBoxLayout()
        self.create_model.setObjectName(u"create_model")
        self.field_search_layout = QVBoxLayout()
        self.field_search_layout.setObjectName(u"field_search_layout")
        self.field_search_label = QLabel(self.centralwidget)
        self.field_search_label.setObjectName(u"field_search_label")
        self.field_search_label.setTextFormat(Qt.PlainText)

        self.field_search_layout.addWidget(self.field_search_label)

        self.field_file_layout = QHBoxLayout()
        self.field_file_layout.setObjectName(u"field_file_layout")
        self.field_search_file_line = QLineEdit(self.centralwidget)
        self.field_search_file_line.setObjectName(u"field_search_file_line")
        self.field_search_file_line.setReadOnly(True)

        self.field_file_layout.addWidget(self.field_search_file_line)

        self.field_file_button = QPushButton(self.centralwidget)
        self.field_file_button.setObjectName(u"field_file_button")

        self.field_file_layout.addWidget(self.field_file_button)

        self.field_search_layout.addLayout(self.field_file_layout)

        self.create_model.addLayout(self.field_search_layout)

        self.pano_search_layout = QVBoxLayout()
        self.pano_search_layout.setObjectName(u"pano_search_layout")
        self.pano_list_search_label = QLabel(self.centralwidget)
        self.pano_list_search_label.setObjectName(u"pano_list_search_label")

        self.pano_search_layout.addWidget(self.pano_list_search_label)

        self.pano_file_layout = QHBoxLayout()
        self.pano_file_layout.setObjectName(u"pano_file_layout")
        self.pano_search_file_line = QLineEdit(self.centralwidget)
        self.pano_search_file_line.setObjectName(u"pano_search_file_line")
        self.pano_search_file_line.setReadOnly(True)

        self.pano_file_layout.addWidget(self.pano_search_file_line)

        self.pano_file_button = QPushButton(self.centralwidget)
        self.pano_file_button.setObjectName(u"pano_file_button")

        self.pano_file_layout.addWidget(self.pano_file_button)

        self.pano_search_layout.addLayout(self.pano_file_layout)

        self.create_model.addLayout(self.pano_search_layout)

        self.create_FOV_error_label = QLabel(self.centralwidget)
        self.create_FOV_error_label.setObjectName(u"create_FOV_error_label")

        self.create_model.addWidget(self.create_FOV_error_label)

        self.create_FOV_button = QPushButton(self.centralwidget)
        self.create_FOV_button.setObjectName(u"create_FOV_button")

        self.create_model.addWidget(self.create_FOV_button)

        self.create_DOF_error_label = QLabel(self.centralwidget)
        self.create_DOF_error_label.setObjectName(u"create_DOF_error_label")

        self.create_model.addWidget(self.create_DOF_error_label)

        self.create_DOF_button = QPushButton(self.centralwidget)
        self.create_DOF_button.setObjectName(u"create_DOF_button")

        self.create_model.addWidget(self.create_DOF_button)

        self.right_layout.addLayout(self.create_model)

        self.main_layout.addLayout(self.right_layout)

        self.verticalLayout.addLayout(self.main_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pano_list_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0421\u043f\u0438\u0441\u043e\u043a \u043f\u0430\u043d\u043e\u0440\u0430\u043c\u043d\u044b\u0445 \u0441\u0438\u0441\u0442\u0435\u043c",
                None))
        self.pano_list_create_button.setText(
            QCoreApplication.translate(
                "MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c",
                None))
        self.pano_list_load_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
                None))
        self.pano_list_clear_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.pano_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u041f\u0430\u043d\u043e\u0440\u0430\u043c\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430",
                None))
        self.pano_add_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.pano_change_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pano_remove_button.setText(
            QCoreApplication.translate(
                "MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
                None))
        self.camera_label.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u041a\u0430\u043c\u0435\u0440\u0430",
                                       None))
        self.camera_add_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.camera_change_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.camera_remove_button.setText(
            QCoreApplication.translate(
                "MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
                None))
        self.label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0421\u043f\u0438\u0441\u043e\u043a \u043f\u0430\u043d\u043e\u0440\u0430\u043c\u043d\u044b\u0445 \u0441\u0438\u0441\u0442\u0435\u043c",
                None))
        self.pano_list_save_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
                None))
        self.pano_list_save_as_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a...",
                None))
        self.field_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0424\u0443\u0442\u0431\u043e\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435",
                None))
        self.field_create_button.setText(
            QCoreApplication.translate(
                "MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c",
                None))
        self.field_load_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
                None))
        self.empty_label.setText("")
        self.field_search_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0412\u044b\u0431\u043e\u0440 \u0444\u0443\u0442\u0431\u043e\u043b\u044c\u043d\u043e\u0433\u043e \u043f\u043e\u043b\u044f",
                None))
        self.field_file_button.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u041f\u043e\u0438\u0441\u043a...",
                                       None))
        self.pano_list_search_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u0412\u044b\u0431\u043e\u0440 \u0441\u043f\u0438\u0441\u043a\u0430 \u043f\u0430\u043d\u043e\u0440\u0430\u043c\u043d\u044b\u0445 \u0441\u0438\u0441\u0442\u0435\u043c",
                None))
        self.pano_file_button.setText(
            QCoreApplication.translate("MainWindow",
                                       u"\u041f\u043e\u0438\u0441\u043a...",
                                       None))
        self.create_FOV_error_label.setText("")
        self.create_FOV_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c FOV",
                None))
        self.create_DOF_error_label.setText("")
        self.create_DOF_button.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c FOS",
                None))

    # retranslateUi
