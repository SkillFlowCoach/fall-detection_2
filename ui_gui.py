# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guiWTZkir.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 70))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.source_txt = QLineEdit(self.frame_2)
        self.source_txt.setObjectName(u"source_txt")
        font = QFont()
        font.setPointSize(12)
        self.source_txt.setFont(font)

        self.horizontalLayout.addWidget(self.source_txt)

        self.select_video_btn = QPushButton(self.frame_2)
        self.select_video_btn.setObjectName(u"select_video_btn")
        self.select_video_btn.setMinimumSize(QSize(150, 0))
        self.select_video_btn.setFont(font)

        self.horizontalLayout.addWidget(self.select_video_btn)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.camera_lbl = QLabel(self.frame)
        self.camera_lbl.setObjectName(u"camera_lbl")
        self.camera_lbl.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.camera_lbl)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 80))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.start_btn = QPushButton(self.frame_3)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setMinimumSize(QSize(200, 0))
        self.start_btn.setFont(font)
        self.start_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.start_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.select_video_btn.setText(QCoreApplication.translate("MainWindow", u"Select video", None))
        self.camera_lbl.setText("")
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

