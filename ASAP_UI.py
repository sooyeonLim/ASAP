# -*- coding: utf-8 -*-
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
#
# version : 2023.10.10

import os, sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import *
from pyqtgraph import GraphicsLayoutWidget,PlotWidget,PlotItem
import pyqtgraph as pg

from hyperspy.io import load as hsload
from asap import ASAP

class Ui_MainWindow(QtWidgets.QMainWindow):


  def __init__(self):
    super().__init__()
    self.setupUi()


  def setupUi(self):
    self.data_num = 0
    self.setObjectName("MainWindow")
    self.resize(1500, 980)
    self.setWindowTitle("Auto Selected Area diffraction patterns Profiler (ASAP)")
    self.setWindowIcon(QIcon("./UI/kist.png"))
    self.centralwidget = QtWidgets.QWidget( )
    self.centralwidget.setObjectName("centralwidget")
    self.setCentralWidget(self.centralwidget)
    self.menubar = QtWidgets.QMenuBar(self)
    self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
    self.menubar.setObjectName("menubar")
    self.setMenuBar(self.menubar)
    self.statusbar = QtWidgets.QStatusBar(self)
    self.statusbar.setObjectName("statusbar")
    self.setStatusBar(self.statusbar)


    #########################################################
    ############          Initialize           ##############
    #########################################################

    self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
    self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 80, 221, 41))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(15)
    self.verticalLayoutWidget_2.setFont(font)
    self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
    self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
    self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
    self.pushButton.setEnabled(True)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
    self.pushButton.setSizePolicy(sizePolicy)
    font = QtGui.QFont("Helvetica")
    font.setPointSize(11)
    self.pushButton.setFont(font)
    self.pushButton.setMouseTracking(False)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./UI/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pushButton.setIcon(icon)
    self.pushButton.setObjectName("pushButton")
    self.pushButton.clicked.connect(self.click_initialize) 
    self.pushButton.setText("Initialize")


    #########################################################
    #############          Load Data           ##############
    #########################################################

    self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
    self.groupBox.setGeometry(QtCore.QRect(20, 170, 261, 211))
    font = QtGui.QFont("Helvetica") 
    font.setPointSize(15)
    font.setBold(True)
    font.setWeight(75)
    self.groupBox.setFont(font)
    self.groupBox.setTitle("Load Data")
    self.groupBox.setObjectName("groupBox")

    self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox)
    self.textBrowser_3.setGeometry(QtCore.QRect(10, 80, 181, 51))
    font = QtGui.QFont()
    font.setPointSize(11)
    font.setBold(False)
    font.setWeight(50)
    self.textBrowser_3.setFont(font)
    self.textBrowser_3.setObjectName("textBrowser_3")
    # self.textBrowser_3.setText("load dm file")
    self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
    self.pushButton_5.setGeometry(QtCore.QRect(200, 80, 51, 51))
    font = QtGui.QFont()
    font.setPointSize(15)
    font.setBold(False)
    font.setWeight(50)
    self.pushButton_5.setFont(font)
    self.pushButton_5.setText("")
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap("./UI/search_color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.pushButton_5.setIcon(icon1)
    self.pushButton_5.setIconSize(QtCore.QSize(30, 30))
    self.pushButton_5.setObjectName("pushButton_5")
    self.pushButton_5.clicked.connect(self.click_dataload) 


    #########################################################
    ################         Profile         ################
    #########################################################

    self.verticalLayout_2.addWidget(self.pushButton)
    self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
    self.groupBox_3.setGeometry(QtCore.QRect(20, 430, 261, 191))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(15)
    font.setBold(True)
    font.setWeight(75)
    self.groupBox_3.setFont(font)
    self.groupBox_3.setTitle("Profile")
    self.groupBox_3.setObjectName("groupBox_3")

    self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
    self.pushButton_2.setEnabled(True)
    self.pushButton_2.setGeometry(QtCore.QRect(20, 80, 221, 51))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(10)
    font.setBold(False)
    font.setWeight(50)
    self.pushButton_2.setFont(font)
    self.pushButton_2.setText("Start")
    self.pushButton_2.setObjectName("pushButton_2")
    self.pushButton_2.clicked.connect(self.click_start) 
  

    #########################################################
    #############            Save Data           ############
    #########################################################

    self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
    self.groupBox_4.setGeometry(QtCore.QRect(20, 670, 261, 261))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(15)
    font.setBold(True)
    font.setWeight(75)
    self.groupBox_4.setFont(font)
    self.groupBox_4.setTitle("Save")
    self.groupBox_4.setObjectName("groupBox_4")

    self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_4)
    self.pushButton_3.setGeometry(QtCore.QRect(20, 40, 221, 51))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(10)
    font.setBold(False)
    font.setWeight(50)
    self.pushButton_3.setFont(font)
    self.pushButton_3.setFlat(False)
    self.pushButton_3.setText("center image (.png)")
    self.pushButton_3.setObjectName("pushButton_3")
    self.pushButton_3.clicked.connect(self.click_save_center) 

    self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
    self.pushButton_4.setGeometry(QtCore.QRect(20, 110, 221, 51))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(10)
    font.setBold(False)
    font.setWeight(50)
    self.pushButton_4.setFont(font)
    self.pushButton_4.setText("save image (.png) ")
    self.pushButton_4.setObjectName("pushButton_4")
    self.pushButton_4.clicked.connect(self.click_save_image) 

    self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_4)
    self.pushButton_6.setGeometry(QtCore.QRect(20, 180, 221, 51))
    font = QtGui.QFont("Helvetica")
    font.setPointSize(10)
    font.setBold(False)
    font.setWeight(50)
    self.pushButton_6.setFont(font)
    self.pushButton_6.setText("save spectrum (.csv) ")
    self.pushButton_6.setObjectName("pushButton_6")
    self.pushButton_6.clicked.connect(self.click_save_spectrum) 

    
    #########################################################
    ###########          Left Groupbox          #############
    #########################################################

    self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
    self.groupBox_6.setGeometry(QtCore.QRect(300, 20, 581, 911))
    font = QtGui.QFont()
    font.setPointSize(15)
    self.groupBox_6.setFont(font)
    self.groupBox_6.setTitle("")
    self.groupBox_6.setObjectName("groupBox_6")

    # original image
    self.label_10 = QtWidgets.QLabel(self.groupBox_6)
    self.label_10.setGeometry(QtCore.QRect(10, 10, 551, 41))
    font = QtGui.QFont("Cambria")
    font.setPointSize(14)
    font.setBold(True)
    font.setWeight(75)
    self.label_10.setFont(font)
    self.label_10.setObjectName("label_10")
    self.label_10.setText("original image :")

    #  plot - original image
    self.imageView = GraphicsLayoutWidget(self.groupBox_6)
    self.imageView.setGeometry(QtCore.QRect(20, 140, 541, 451))
    self.imageView.setObjectName("imageView")

    # slide 
    self.horizontalSlider_2 = QtWidgets.QSlider(self.groupBox_6)
    self.horizontalSlider_2.setGeometry(QtCore.QRect(20, 70, 381, 41))
    font = QtGui.QFont()
    font.setPointSize(15)
    self.horizontalSlider_2.setFont(font)
    self.horizontalSlider_2.setMouseTracking(True)
    self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
    self.horizontalSlider_2.setMaximum(0)
    self.horizontalSlider_2.setMinimum(0)
    self.horizontalSlider_2.setObjectName("horizontalSlider_2")
    self.spinBox = QtWidgets.QSpinBox(self.groupBox_6)
    self.spinBox.setGeometry(QtCore.QRect(430, 70, 111, 41))
    self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
    self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
    self.spinBox.setProperty("showGroupSeparator", False)
    self.spinBox.setMinimum(0)
    self.spinBox.setMaximum(0)
    self.spinBox.setObjectName("spinBox")
    self.horizontalSlider_2.valueChanged.connect(self.spinBox.setValue)
    self.spinBox.valueChanged.connect(self.horizontalSlider_2.setValue)

    # original center / restored center (transmission point)
    self.label = QtWidgets.QLabel(self.groupBox_6)
    self.label.setGeometry(QtCore.QRect(20, 610, 261, 31))
    font = QtGui.QFont("Cambria")
    font.setPointSize(11)
    font.setBold(True)
    font.setWeight(75)
    self.label.setFont(font)
    self.label.setObjectName("label")
    self.label.setText("original center ")
    self.label_2 = QtWidgets.QLabel(self.groupBox_6)
    self.label_2.setGeometry(QtCore.QRect(300, 610, 261, 31))
    font = QtGui.QFont("Cambria")
    font.setPointSize(11)
    font.setBold(True)
    font.setWeight(75)
    self.label_2.setFont(font)
    self.label_2.setObjectName("label_2")
    self.label_2.setText("restored center")

    # plot 
    self.imageView_3 = GraphicsLayoutWidget(self.groupBox_6)
    self.imageView_3.setGeometry(QtCore.QRect(20, 650, 261, 231))
    self.imageView_3.setObjectName("imageView_3")
    self.imageView_4 = GraphicsLayoutWidget(self.groupBox_6)
    self.imageView_4.setGeometry(QtCore.QRect(300, 650, 261, 231))
    self.imageView_4.setObjectName("imageView_4")


    #########################################################
    ###########          Right Groupbox          ############
    #########################################################

    self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
    self.groupBox_5.setGeometry(QtCore.QRect(900, 20, 591, 911))
    font = QtGui.QFont()
    font.setPointSize(15)
    self.groupBox_5.setFont(font)
    self.groupBox_5.setTitle("")
    self.groupBox_5.setObjectName("groupBox_5")
    self.label_8 = QtWidgets.QLabel(self.groupBox_5)
    self.label_8.setGeometry(QtCore.QRect(10, 10, 571, 41))
    font = QtGui.QFont("Cambria")
    font.setPointSize(14)
    font.setBold(True)
    font.setWeight(75)
    self.label_8.setFont(font)
    self.label_8.setText("restored image :")
    self.label_8.setObjectName("label_8")

    # slide
    self.horizontalSlider = QtWidgets.QSlider(self.groupBox_5)
    self.horizontalSlider.setGeometry(QtCore.QRect(30, 70, 381, 41))
    font = QtGui.QFont()
    font.setPointSize(15)
    self.horizontalSlider.setFont(font)
    self.horizontalSlider.setMouseTracking(True)
    self.horizontalSlider.setAcceptDrops(False)
    self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
    self.horizontalSlider.setMaximum(0)
    self.horizontalSlider.setMinimum(0)
    self.horizontalSlider.setObjectName("horizontalSlider")
    self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox_5)
    self.spinBox_2.setGeometry(QtCore.QRect(440, 70, 111, 41))
    self.spinBox_2.setAlignment(QtCore.Qt.AlignCenter)
    self.spinBox_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
    self.spinBox_2.setProperty("showGroupSeparator", False)
    self.spinBox_2.setMinimum(0)
    self.spinBox_2.setMaximum(0)
    self.spinBox_2.setObjectName("spinBox_2")
    self.horizontalSlider.valueChanged.connect(self.spinBox_2.setValue)
    self.spinBox_2.valueChanged.connect(self.horizontalSlider.setValue)

    # plot - restored image /  profiled spectrum
    self.imageView_2 = GraphicsLayoutWidget(self.groupBox_5)
    self.imageView_2.setGeometry(QtCore.QRect(20, 140, 541, 451))
    self.imageView_2.setObjectName("imageView_2")
    self.imageView_5 = GraphicsLayoutWidget(self.groupBox_5)
    self.imageView_5.setGeometry(QtCore.QRect(20, 650, 541, 231))
    self.imageView_5.setObjectName("imageView_5")
    self.label_3 = QtWidgets.QLabel(self.groupBox_5)
    self.label_3.setGeometry(QtCore.QRect(20, 610, 541, 31))
    font = QtGui.QFont("Cambria")
    font.setPointSize(11)
    font.setBold(True)
    font.setWeight(75)
    self.label_3.setFont(font)
    self.label_3.setText("profiled spectrum")
    self.label_3.setObjectName("label_3")

    self.retranslateUi()
    QtCore.QMetaObject.connectSlotsByName(self)
    self.show()


  #########################################################
  ############            Functions            ############
  #########################################################

  def retranslateUi(self):
      _translate = QtCore.QCoreApplication.translate
      self.groupBox.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>d</p></body></html>"))


  def click_initialize(self):
    self.setupUi()


  def click_dataload(self):
    self.statusbar.showMessage("loading ...")
    # self.progressbar = QtWidgets.QProgressBar()
    # self.progressbar.setMinimum(0)
    # self.progressbar.setMaximum(0)
    # self.statusbar.addWidget(self.progressbar)

    _translate = QtCore.QCoreApplication.translate
    fnames=QFileDialog.getOpenFileNames(self, 'open file','./')
    path_list = []
    for i in fnames[0]:
        base, ext = os.path.splitext(i)
        if len(ext)>0 and (ext=='.dm4' or ext=='.dm3') :
            self.data_num += 1
            path_list.append(i)

    self.fnames = path_list
    self.horizontalSlider_2.setRange(1, self.data_num)       # set slider range 
    self.spinBox.setRange(1, self.data_num)
    self.textBrowser_3.setText(_translate("MainWindow", "loaded {} files".format(self.data_num)))

    org_images = []
    for i in self.fnames:
      s= hsload(i)
      axes = s.axes_manager.as_dictionary()
      self.scale = next((item.get('scale') for item in axes.values() if item.get('name')=='x'),1)
      org_images.append(s.data.copy())
      self.distance_limit = int(s.data.shape[0]/8)
      self.kernel_blur = int(s.data.shape[0]/32)
      self.smallradii = int(self.kernel_blur/10)
      self.kernel_beamstop = int(s.data.shape[0]/1024) if s.data.shape[0]>1024 else 1
      self.find_circle_ratio = 2 # 2.2 sigma
    self.org_images = np.array(org_images)
    self.plot_view_1()
    self.horizontalSlider_2.sliderMoved.connect(self.plot_view_1)   # connect slider-image
    self.spinBox.valueChanged.connect(self.plot_view_1)

    self.statusbar.clearMessage()
    # self.statusbar.removeWidget(self.progressbar)


  def click_start(self):
    self.statusbar.showMessage(" processing ...")

    centers = []
    x_axis_s = []
    radialprofile_s = []
    merged_image_s = []
    for f in self.fnames:
      k = ASAP(f)
      k.auto_profile()
      (x_axis, radialprofile) = k.radial_profile(center = k.center)
      centers.append(k.center)
      x_axis_s.append(x_axis)
      radialprofile_s.append(radialprofile)
      merged_image_s.append(k.merged_image)

    self.centers = np.array(centers)
    self.x_axis_s = x_axis_s
    self.radialprofile_s = radialprofile_s
    self.merged_image = np.array(k.merged_image)
    self.merged_image = np.array(merged_image_s)


    # set right slider range 
    self.horizontalSlider.setRange(1, self.data_num) 
    self.spinBox_2.setRange(1, self.data_num)
    self.horizontalSlider.valueChanged.connect(self.spinBox_2.setValue)
    self.spinBox_2.valueChanged.connect(self.horizontalSlider.setValue)
    self.horizontalSlider.setValue(self.horizontalSlider_2.value())
    self.spinBox_2.setValue(self.spinBox.value())

    self.horizontalSlider_2.valueChanged.connect(self.horizontalSlider.setValue)
    self.spinBox_2.valueChanged.connect(self.spinBox.setValue)

    self.plot_view_3()
    self.horizontalSlider_2.sliderMoved.connect(self.plot_view_3)
    self.spinBox.valueChanged.connect(self.plot_view_3)
    self.plot_view_4()
    self.horizontalSlider_2.sliderMoved.connect(self.plot_view_4)
    self.spinBox.valueChanged.connect(self.plot_view_4)

    self.plot_view_2()
    self.horizontalSlider.sliderMoved.connect(self.plot_view_2)
    self.spinBox_2.valueChanged.connect(self.plot_view_2)
    self.plot_view_5()
    self.horizontalSlider.sliderMoved.connect(self.plot_view_5)
    self.spinBox_2.valueChanged.connect(self.plot_view_5)

    self.statusbar.clearMessage()


  def plot_view_1(self):
    """original SADP image"""
    order = int(self.spinBox.value()-1)
    org_image = self.org_images[order]
    self.p = pg.ViewBox(enableMouse=False,invertY=False,lockAspect = True,defaultPadding=0) 
    self.imageView.setCentralItem(self.p)
    plot_widget = pg.ImageItem(image= org_image, axisOrder='row-major')
    self.p.addItem(plot_widget)
    self.p._updateView


  def plot_view_3(self):
    """original transmission point"""
    order = int(self.spinBox.value()-1)
    center = self.centers[order]
    center_x, center_y = int(center[0]), int(center[1])
    range = 600
    org_image = self.org_images[order]
    org_center = int(len(org_image)/2)
    plot_image = org_image[org_center-range : org_center+range,org_center-range : org_center+range]
    self.p = pg.ViewBox(enableMouse=False,invertY=False,lockAspect = True, defaultPadding=0) 
    self.imageView_3.setCentralItem(self.p)
    plot_widget = pg.ImageItem(image= plot_image, axisOrder='row-major')
    self.p.addItem(plot_widget)

    x = np.array([int(len(plot_image)/2), int(len(plot_image)/2)])
    y = np.array([0, len(plot_image)])
    vertical_line = pg.PlotCurveItem(x,y , pen=pg.mkPen(color=(1, 164, 250, 150), width=1, style=QtCore.Qt.DashLine))
    horizontal_line = pg.PlotCurveItem(y,x , pen=pg.mkPen(color=(1, 164, 250, 150), width=1, style=QtCore.Qt.DashLine))
    self.p.addItem(vertical_line)
    self.p.addItem(horizontal_line) 

    self.p._updateView

    
  def plot_view_4(self):
    """restored transmission point"""
    order = int(self.spinBox.value()-1)
    center = self.centers[order]
    center_x, center_y = int(center[1]), int(center[0])
    range = 600
    org_image = self.org_images[order][center_x-range : center_x+range,center_y-range : center_y+range]
    self.p = pg.ViewBox(enableMouse=False,invertY=False,lockAspect = True, defaultPadding=0) 
    self.imageView_4.setCentralItem(self.p)
    plot_widget = pg.ImageItem(image= org_image, axisOrder='row-major')
    self.p.addItem(plot_widget)

    x = np.array([int(len(org_image)/2), int(len(org_image)/2)])
    y = np.array([0, len(org_image)])
    vertical_line = pg.PlotCurveItem(x,y , pen=pg.mkPen(color=(1, 164, 250, 150), width=1, style=QtCore.Qt.DashLine))
    horizontal_line = pg.PlotCurveItem(y,x , pen=pg.mkPen(color=(1, 164, 250, 150), width=1, style=QtCore.Qt.DashLine))
    self.p.addItem(vertical_line)
    self.p.addItem(horizontal_line) 

    self.p._updateView


  def plot_view_2(self):
    """restored SADP image"""
    order = int(self.spinBox_2.value()-1)
    org_image = self.merged_image[order]
    self.p = pg.ViewBox(enableMouse=False,invertY=False,lockAspect = True,defaultPadding=0) 
    self.imageView_2.setCentralItem(self.p)
    plot_widget = pg.ImageItem(image= org_image, axisOrder='row-major')
    self.p.addItem(plot_widget)
    self.p._updateView

  def plot_view_5(self):
    """profiled spectrum"""
    order = int(self.spinBox_2.value()-1)
    self.plot_widget = pg.ViewBox()
    self.imageView_5.setCentralWidget(self.plot_widget)
    plot_widget = pg.PlotDataItem(x = self.x_axis_s[order], y = self.radialprofile_s[order])
    self.plot_widget.addItem(plot_widget)
    self.plot_widget._updateView

  def click_save_center(self):
    order = int(self.spinBox_2.value()-1)
    center = self.centers[order]
    center_x, center_y = int(center[1]), int(center[0])
    range = 600
    org_image = self.org_images[order][center_x-range : center_x+range,center_y-range : center_y+range]
    fname=QFileDialog.getSaveFileName(self, 'save center image','./')
    plt.imshow(org_image, cmap='grey')
    plt.axis('off')
    plt.savefig(fname[0],bbox_inches = 'tight', pad_inches = 0)
    

  def click_save_image(self):
    order = int(self.spinBox_2.value()-1)
    org_image = self.merged_image[order]
    fname=QFileDialog.getSaveFileName(self, 'save SADP image','./')
    plt.imshow(org_image, cmap='grey')
    plt.axis('off')
    plt.savefig(fname[0],bbox_inches = 'tight', pad_inches = 0)


  def click_save_spectrum(self):
    order = int(self.spinBox_2.value()-1)
    x = self.x_axis_s[order]
    y = self.radialprofile_s[order]
    fname=QFileDialog.getSaveFileName(self, 'save SADP spectrum','./')
    import pandas as pd
    df = pd.DataFrame({'x_axis':x, 'y_axis':y})
    df.to_csv(fname[0], index=False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    import qdarktheme
    # app.setStyleSheet(qdarktheme.load_stylesheet(border="sharp"))
    app.setStyleSheet(qdarktheme.load_stylesheet(corner_shape="sharp"))
    ui = Ui_MainWindow()

    sys.exit(app.exec_())

