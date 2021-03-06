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
from qgis.core import QgsMapLayerRegistry
import processing


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Desire_lines_dockwidget_base.ui'))


class DesirelinesDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(DesirelinesDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.legend = self.iface.legendInterface()

        self.create = self.pushButton_4
        self.selectextent = self.pushButton_5
        self.selectLayer = self.comboBox
        self.firstMeasure = self.comboBox_2
        self.firstCheck = self.checkBox
        self.firstSpinBox = self.doubleSpinBox
        self.secondMeasure = self.comboBox_3
        self.secondCheck = self.checkBox_2
        self.secondSpinBox = self.doubleSpinBox_2
        self.applyThreshold = self.pushButton
        self.interval = self.spinBox
        self.top = self.doubleSpinBox_4
        self.bottom = self.doubleSpinBox_5
        self.applySymbology = self.pushButton_2
        self.savelocationText = self.lineEdit
        self.saveLocation = self.pushButton_3

        self.updateLayer()
        self.initialisations()


        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.updateLayer)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.updateLayer)
        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.initialisations)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.initialisations)

        self.selectextent.clicked.connect(self.selectByRadius)
        self.create.clicked.connect(self.activateButtons)
        self.create.clicked.connect(self.saveSelection)

    def initialisations(self):
        if self.selectLayer.count() == 0:
            self.selectextent.setEnabled(False)
            self.create.setEnabled(False)
            self.selectextent.setEnabled(False)
            self.selectLayer.setEnabled(False)
            self.firstMeasure.setEnabled(False)
            self.firstCheck.setEnabled(False)
            self.firstSpinBox.setEnabled(False)
            self.secondMeasure.setEnabled(False)
            self.secondCheck.setEnabled(False)
            self.secondSpinBox.setEnabled(False)
            self.applyThreshold.setEnabled(False)
            self.interval.setEnabled(False)
            self.top.setEnabled(False)
            self.bottom.setEnabled(False)
            self.applySymbology.setEnabled(False)
            self.savelocationText.setEnabled(False)
            self.saveLocation.setEnabled(False)


        else:
            self.selectextent.setEnabled(True)
            self.create.setEnabled(True)
            self.selectextent.setEnabled(True)
            self.selectLayer.setEnabled(True)



    def activateButtons(self):
        self.selectextent.setEnabled(True)
        self.firstMeasure.setEnabled(True)
        self.firstCheck.setEnabled(True)
        self.firstSpinBox.setEnabled(True)
        self.secondMeasure.setEnabled(True)
        self.secondCheck.setEnabled(True)
        self.secondSpinBox.setEnabled(True)
        self.applyThreshold.setEnabled(True)
        self.interval.setEnabled(True)
        self.top.setEnabled(True)
        self.bottom.setEnabled(True)
        self.applySymbology.setEnabled(True)
        self.savelocationText.setEnabled(True)
        self.saveLocation.setEnabled(True)

    def setLayer(self):
        # get the new layer
        index = self.selectLayer.currentIndex()
        self.selectedLayer = self.selectLayer.itemData(index)
        return self.selectedLayer

    # Add  layer to combobox if conditions are satisfied
    def updateLayer(self):
        self.selectLayer.clear()
        self.selectLayer.setEnabled(False)
        layers = self.legend.layers()

        for lyr in layers:
            if uf.isRequiredLayer(self.iface, lyr):
                self.selectLayer.addItem(lyr.name(), lyr)

        if self.selectLayer.count() > 0:
            self.selectLayer.setEnabled(True)
            self.layer = self.setLayer()


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
        QgsMapLayerRegistry.instance().legendLayersAdded.disconnect(self.updateLayer)
        QgsMapLayerRegistry.instance().layersRemoved.disconnect(self.updateLayer)

    def selectByRadius(self):
        if self.selectLayer.count() > 0:
            self.selectextent.setEnabled(True)
            self.iface.actionSelectRadius().trigger()

    def saveSelection(self):
        layer = self.setLayer()
        selectedLines = processing.runalg('qgis:saveselectedfeatures', layer, None)
        filename = os.path.basename(selectedLines['OUTPUT_LAYER'])
        location = os.path.abspath(selectedLines['OUTPUT_LAYER'])
        result_layer = self.iface.addVectorLayer(location, filename, "ogr")
        result_layer.setLayerName("memory:Desire Lines")



