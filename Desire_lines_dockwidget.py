# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DesirelinesDockWidget
                                 A QGIS plugin
 Create the desire lines from a space Syntax accessibility analysis
                             -------------------
        begin                : 2018-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2018 by AA/Space Syntax Limited
        email                : a.acharya@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from . import utility_functions as uf

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Desire_lines_dockwidget_base.ui'))


class DesirelinesDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(DesirelinesDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        selectLayer = self.comboBox()
        firstMeasure = self.comboBox_2()
        firstCheck = self.checkBox()
        firstSpinBox = self.doubleSpinBox()
        secondMeasure = self.comboBox_3()
        secondCheck = self.checkBox_2()
        secondSpinBox = self.doubleSpinBox_2()
        applyThreshold = self.pushButton()
        interval = self.spinBox()
        top = self.doubleSpinBox_4()
        bottom = self.doubleSpinBox_5()
        applySymbology = self.pushButton_2()
        savelocationText = self.lineEdit()
        saveLocation = self.pushButton_3()



    def setLayer(self):
        # get the new layer
        index = self.comboBox().currentIndex()
        self.selectedLayer = self.comboBox().itemData(index)
        return self.selectedLayer

    # Add Frontage layer to combobox if conditions are satisfied
    def updateFrontageLayer(self):
        self.dockwidget.useExistingcomboBox.clear()
        self.dockwidget.useExistingcomboBox.setEnabled(False)
        self.disconnectFrontageLayer()
        layers = self.legend.layers()
        type = 1
        for lyr in layers:
            if uf.isRequiredLayer(self.iface, lyr, type):
                self.dockwidget.useExistingcomboBox.addItem(lyr.name(), lyr)

        if self.dockwidget.useExistingcomboBox.count() > 0:
            self.dockwidget.useExistingcomboBox.setEnabled(True)
            self.frontage_layer = self.dockwidget.setFrontageLayer()
            self.connectFrontageLayer()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

