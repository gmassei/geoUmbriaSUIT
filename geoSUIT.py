# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name            : geoUmbriaSUIT
Description        : geographical MCDA for sustainability assessment
Date            : June 16, 2013
copyright        : ARPA Umbria - Università degli Studi di Perugia (C) 2013
email            : (developper) Gianluca Massei (g_massa@libero.it)

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui

from qgis.core import *
from qgis.gui import *

import numpy as np
import webbrowser
import matplotlib.pyplot as plt
import os


import DOMLEM
import htmlGraph

from ui_geoSUIT import Ui_Dialog

class geoSUITDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        '''costruttore'''
        QDialog.__init__(self, iface.mainWindow())
        self.setupUi(self)
        self.iface = iface
        self.active_layer = self.iface.activeLayer()
        self.base_Layer = self.iface.activeLayer()
        for i in range(1,self.toolBox.count()):
            self.toolBox.setItemEnabled (i,False)

        QObject.connect(self.RetriveFileTBtn, SIGNAL( "clicked()" ), self.outFile)
        QObject.connect(self.SetBtnBox, SIGNAL("accepted()"), self.settingStart)
        QObject.connect(self.SetBtnBox, SIGNAL("rejected()"),self, SLOT("reject()"))
        QObject.connect(self.SetBtnAbout, SIGNAL("clicked()"), self.about)
        QObject.connect(self.SetBtnHelp, SIGNAL("clicked()"),self.open_help)
        QObject.connect(self.EnvSaveCfgBtn, SIGNAL("clicked()"),self.SaveCfg)
        QObject.connect(self.EcoSaveCfgBtn, SIGNAL("clicked()"),self.SaveCfg)
        QObject.connect(self.SocSaveCfgBtn, SIGNAL("clicked()"),self.SaveCfg)

        QObject.connect(self.EnvAddFieldBtn, SIGNAL( "clicked()" ), self.AddField)
        QObject.connect(self.EnvRemoveFieldBtn, SIGNAL( "clicked()" ), self.RemoveField)
        QObject.connect(self.EnvCalculateBtn, SIGNAL( "clicked()" ), self.AnalyticHierarchyProcess)
        QObject.connect(self.EnvGetWeightBtn, SIGNAL( "clicked()" ), self.Elaborate)

        QObject.connect(self.EcoAddFieldBtn, SIGNAL( "clicked()" ), self.AddField)
        QObject.connect(self.EcoRemoveFieldBtn, SIGNAL( "clicked()" ), self.RemoveField)
        QObject.connect(self.EcoCalculateBtn, SIGNAL( "clicked()" ), self.AnalyticHierarchyProcess)
        QObject.connect(self.EcoGetWeightBtn, SIGNAL( "clicked()" ), self.Elaborate)

        QObject.connect(self.SocAddFieldBtn, SIGNAL( "clicked()" ), self.AddField)
        QObject.connect(self.SocRemoveFieldBtn, SIGNAL( "clicked()" ), self.RemoveField)
        QObject.connect(self.SocCalculateBtn, SIGNAL( "clicked()" ), self.AnalyticHierarchyProcess)
        QObject.connect(self.SocGetWeightBtn, SIGNAL( "clicked()" ), self.Elaborate)

        QObject.connect(self.RenderBtn,SIGNAL("clicked()"), self.RenderLayer)
        QObject.connect(self.GraphBtn, SIGNAL("clicked()"), self.BuildOutput)

        QObject.connect(self.AnlsBtnBox, SIGNAL("rejected()"),self, SLOT("reject()"))
        QObject.connect(self.CritExtractBtn, SIGNAL( "clicked()" ), self.ExtractRules)
        
        sourceIn=str(self.iface.activeLayer().source())
        self.BaseLayerLbl.setText(sourceIn)
        
        self.baseLbl.setText(sourceIn)
        pathSource=os.path.dirname(sourceIn)
        outputFile="geosustainability.shp"
        sourceOut=os.path.join(pathSource,outputFile)
        self.OutlEdt.setText(str(sourceOut))

        self.EnvMapNameLbl.setText(self.active_layer.name())
        self.EcoMapNameLbl.setText(self.active_layer.name())
        self.SocMapNameLbl.setText(self.active_layer.name())

        self.EnvlistFieldsCBox.addItems(self.GetFieldNames(self.active_layer))
        self.EcolistFieldsCBox.addItems(self.GetFieldNames(self.active_layer))
        self.SoclistFieldsCBox.addItems(self.GetFieldNames(self.active_layer))
#################################################################################
        Envfields=self.GetFieldNames(self.active_layer) #field list
        self.EnvTableWidget.setColumnCount(len(Envfields))
        self.EnvTableWidget.setHorizontalHeaderLabels(Envfields)
        self.EnvTableWidget.setRowCount(len(Envfields))
        self.EnvTableWidget.setVerticalHeaderLabels(Envfields)
        EnvSetLabel=["Weigths","Preference"]
        self.EnvWeighTableWidget.setColumnCount(len(Envfields))
        self.EnvWeighTableWidget.setHorizontalHeaderLabels(Envfields)
        self.EnvWeighTableWidget.setRowCount(2)
        self.EnvWeighTableWidget.setVerticalHeaderLabels(EnvSetLabel)
        for r in range(len(Envfields)):
            self.EnvTableWidget.setItem(r,r,QTableWidgetItem("1.0"))
            self.EnvWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
            self.EnvWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))
        #retrieve signal for modified cell
        self.EnvTableWidget.cellChanged[(int,int)].connect(self.CompleteMatrix)
        self.EnvWeighTableWidget.cellClicked[(int,int)].connect(self.ChangeValue)
#################################################################################
        Ecofields=self.GetFieldNames(self.active_layer) #field list
        self.EcoTableWidget.setColumnCount(len(Ecofields))
        self.EcoTableWidget.setHorizontalHeaderLabels(Ecofields)
        self.EcoTableWidget.setRowCount(len(Ecofields))
        self.EcoTableWidget.setVerticalHeaderLabels(Ecofields)
        EcoSetLabel=["Weigths","Preference"]
        self.EcoWeighTableWidget.setColumnCount(len(Ecofields))
        self.EcoWeighTableWidget.setHorizontalHeaderLabels(Ecofields)
        self.EcoWeighTableWidget.setRowCount(2)
        self.EcoWeighTableWidget.setVerticalHeaderLabels(EcoSetLabel)
        for r in range(len(Ecofields)):
            self.EcoTableWidget.setItem(r,r,QTableWidgetItem("1.0"))
            self.EcoWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
            self.EcoWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))
        #retrieve signal for modified cell
        self.EcoTableWidget.cellChanged[(int,int)].connect(self.CompleteMatrix)
        self.EcoWeighTableWidget.cellClicked[(int,int)].connect(self.ChangeValue)
##################################################################################
        Socfields=self.GetFieldNames(self.active_layer) #field list
        self.SocTableWidget.setColumnCount(len(Socfields))
        self.SocTableWidget.setHorizontalHeaderLabels(Socfields)
        self.SocTableWidget.setRowCount(len(Socfields))
        self.SocTableWidget.setVerticalHeaderLabels(Socfields)
        SocSetLabel=["Weigths","Preference"]
        self.SocWeighTableWidget.setColumnCount(len(Socfields))
        self.SocWeighTableWidget.setHorizontalHeaderLabels(Socfields)
        self.SocWeighTableWidget.setRowCount(2)
        self.SocWeighTableWidget.setVerticalHeaderLabels(SocSetLabel)
        for r in range(len(Socfields)):
            self.SocTableWidget.setItem(r,r,QTableWidgetItem("1.0"))
            self.SocWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
            self.SocWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))
        #retrieve signal for modified cell
        self.SocTableWidget.cellChanged[(int,int)].connect(self.CompleteMatrix)
        self.SocWeighTableWidget.cellClicked[(int,int)].connect(self.ChangeValue)

        currentDir=unicode(os.path.abspath( os.path.dirname(__file__)))
        self.LblLogo.setPixmap(QtGui.QPixmap(os.path.join(currentDir,"icon.png")))


    def GetFieldNames(self, layer):
        """retrive field names from active map/layer"""
        fields = layer.dataProvider().fields()
        field_list = []
        for field in fields:
            if field.typeName()!='String':
                field_list.append(str(field.name()))
        return field_list


    def outFile(self):
        """Display file dialog for output  file"""
        self.OutlEdt.clear()
        outvLayer = QFileDialog.getSaveFileName(self, "Output map",".", "ESRI Shapefile (*.shp)")
        self.OutlEdt.insert(outvLayer)
        return outvLayer


    def settingStart(self):
        """ Prepare file for processing """
        outputFilename=self.OutlEdt.text()
        for i in range(1,self.toolBox.count()):
            self.toolBox.setItemEnabled (i,True)
        alayer = self.base_Layer #self.iface.activeLayer()
        provider = alayer.dataProvider()
        fields = provider.fields()
        writer = QgsVectorFileWriter(outputFilename, "CP1250", fields, provider.geometryType(), alayer.crs(), "ESRI Shapefile")
        outFeat = QgsFeature()
        self.LoadProgressBar.setRange(1,alayer.featureCount())
        progress=0
        for inFeat in alayer.getFeatures():
            progress=progress+1
            outFeat.setGeometry(inFeat.geometry() )
            outFeat.setAttributes(inFeat.attributes() )
            writer.addFeature( outFeat )
            self.LoadProgressBar.setValue(progress)
        del writer
        newlayer = QgsVectorLayer(outputFilename, "geosustainability", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(newlayer)
        self.active_layer =newlayer
        self.active_layer=QgsVectorLayer(self.OutlEdt.text(), self.active_layer.name(), "ogr") ##TODO verify
        self.toolBox.setEnabled(True)
        self.updateTable()
        self.LabelListFieldsCBox.addItems(provider.fieldNameMap().keys())
        self.EnvGetWeightBtn.setEnabled(True)
        self.EcoGetWeightBtn.setEnabled(True)
        self.SocGetWeightBtn.setEnabled(True)
        return 0



    def updateTable(self):
        """Prepare and compile tbale in GUI"""
        pathSource=os.path.dirname(str(self.base_Layer.source()))
        if self.preFIXcheckBox.isChecked():
            ENVprefix=self.prefixENVlEdt.text()
            ECOprefix=self.prefixECOlEdt.text()
            SOCprefix=self.prefixECOlEdt.text()
            Envfields=[f for f in self.GetFieldNames(self.active_layer) if f[:len(ENVprefix)]==self.prefixENVlEdt.text()]
            Ecofields=[f for f in self.GetFieldNames(self.active_layer) if f[:len(ECOprefix)]==self.prefixECOlEdt.text()]
            Socfields=[f for f in self.GetFieldNames(self.active_layer) if f[:len(SOCprefix)]==self.prefixSOClEdt.text()]
############################################################################################################################
            self.EnvTableWidget.setColumnCount(len(Envfields))
            self.EnvTableWidget.setHorizontalHeaderLabels(Envfields)
            self.EnvTableWidget.setRowCount(len(Envfields))
            self.EnvTableWidget.setVerticalHeaderLabels(Envfields)
            EnvSetLabel=["Label","Weigths","Preference","Ideal point", "worst point "]
            self.EnvWeighTableWidget.setColumnCount(len(Envfields))
            self.EnvWeighTableWidget.setHorizontalHeaderLabels(Envfields)
            self.EnvWeighTableWidget.setRowCount(5)
            self.EnvWeighTableWidget.setVerticalHeaderLabels(EnvSetLabel)
            if os.path.exists(os.path.join(pathSource,"setting.csv"))==True:
                setting=[i.strip().split(';') for i in open(os.path.join(pathSource,"setting.csv")).readlines()]
                for i in range(len(Envfields)):
                    for l in range(len(setting[1])):
                        if Envfields[i]==setting[1][l]:
                            self.EnvTableWidget.horizontalHeaderItem(i).setToolTip(unicode(str(setting[0][l])))
                            self.EnvTableWidget.verticalHeaderItem(i).setToolTip(unicode(str(setting[0][l])))
                            self.EnvWeighTableWidget.horizontalHeaderItem(i).setToolTip(unicode(str(setting[0][l])))
                            self.EnvWeighTableWidget.setItem(0,i,QTableWidgetItem(str(setting[0][l])))
                            self.EnvWeighTableWidget.setItem(1,i,QTableWidgetItem(str(setting[2][l])))
                            self.EnvWeighTableWidget.setItem(2,i,QTableWidgetItem(str(setting[3][l])))                         
            else:
                for r in range(len(Envfields)):
                    self.EnvWeighTableWidget.setItem(0,r,QTableWidgetItem("-"))
                    self.EnvWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
                    self.EnvWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))

############################################################################################################################
            self.EcoTableWidget.setColumnCount(len(Ecofields))
            self.EcoTableWidget.setHorizontalHeaderLabels(Ecofields)
            self.EcoTableWidget.setRowCount(len(Ecofields))
            self.EcoTableWidget.setVerticalHeaderLabels(Ecofields)
            EcoSetLabel=["Label","Weigths","Preference","Ideal point", "worst point "]
            self.EcoWeighTableWidget.setColumnCount(len(Ecofields))
            self.EcoWeighTableWidget.setHorizontalHeaderLabels(Ecofields)
            self.EcoWeighTableWidget.setRowCount(5)
            self.EcoWeighTableWidget.setVerticalHeaderLabels(EcoSetLabel)

            if os.path.exists(os.path.join(pathSource,"setting.csv"))==True:
                for e in range(len(Ecofields)):
                    for s in range(len(setting[1])):
                        if Ecofields[e]==setting[1][s]:
                            self.EcoTableWidget.horizontalHeaderItem(e).setToolTip((str(setting[0][s])))
                            self.EcoTableWidget.verticalHeaderItem(e).setToolTip((str(setting[0][s])))
                            self.EcoWeighTableWidget.horizontalHeaderItem(e).setToolTip((str(setting[0][s])))
                            self.EcoWeighTableWidget.setItem(0,e,QTableWidgetItem(str(setting[0][s])))
                            self.EcoWeighTableWidget.setItem(1,e,QTableWidgetItem(str(setting[2][s])))
                            self.EcoWeighTableWidget.setItem(2,e,QTableWidgetItem(str(setting[3][s])))
            else:
                for r in range(len(Ecofields)):
                    self.EcoWeighTableWidget.setItem(0,r,QTableWidgetItem("-"))
                    self.EcoWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
                    self.EcoWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))
############################################################################################################################
            self.SocTableWidget.setColumnCount(len(Socfields))
            self.SocTableWidget.setHorizontalHeaderLabels(Socfields)
            self.SocTableWidget.setRowCount(len(Socfields))
            self.SocTableWidget.setVerticalHeaderLabels(Socfields)
            SocSetLabel=["Label","Weigths","Preference","Ideal point", "worst point "]
            self.SocWeighTableWidget.setColumnCount(len(Socfields))
            self.SocWeighTableWidget.setHorizontalHeaderLabels(Socfields)
            self.SocWeighTableWidget.setRowCount(5)
            self.SocWeighTableWidget.setVerticalHeaderLabels(SocSetLabel)

            if os.path.exists(os.path.join(pathSource,"setting.csv"))==True:
                for t in range(len(Socfields)):
                    for q in range(len(setting[1])):
                        if Socfields[t]==setting[1][q]:
                            self.SocTableWidget.horizontalHeaderItem(t).setToolTip((str(setting[0][q])))
                            self.SocTableWidget.verticalHeaderItem(t).setToolTip((str(setting[0][q])))
                            self.SocWeighTableWidget.horizontalHeaderItem(t).setToolTip((str(setting[0][q])))
                            self.SocWeighTableWidget.setItem(0,t,QTableWidgetItem(str(setting[0][q])))
                            self.SocWeighTableWidget.setItem(1,t,QTableWidgetItem(str(setting[2][q])))
                            self.SocWeighTableWidget.setItem(2,t,QTableWidgetItem(str(setting[3][q])))
                            
            else:
                for r in range(len(Socfields)):
                    self.SocWeighTableWidget.setItem(0,r,QTableWidgetItem("-"))
                    self.SocWeighTableWidget.setItem(1,r,QTableWidgetItem("1.0"))
                    self.SocWeighTableWidget.setItem(2,r,QTableWidgetItem("gain"))
        self.updateGUIIdealPoint()
        return 0

    def updateGUIIdealPoint(self):
        provider=self.active_layer.dataProvider()
        ##Environmental
        criteria=[self.EnvTableWidget.verticalHeaderItem(f).text() for f in range(self.EnvTableWidget.columnCount())]
        preference=[str(self.EnvWeighTableWidget.item(2, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())]
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its name
        minField=[provider.minimumValue( f ) for f in fids]
        maxField=[provider.maximumValue( f ) for f in fids]
        for r in range(len(preference)):
            if preference[r]=='gain':
                self.EnvWeighTableWidget.setItem(3,r,QTableWidgetItem(str(maxField[r])))#ideal point
                self.EnvWeighTableWidget.setItem(4,r,QTableWidgetItem(str(minField[r])))#worst point
            elif preference[r]=='cost':
                self.EnvWeighTableWidget.setItem(3,r,QTableWidgetItem(str(minField[r])))
                self.EnvWeighTableWidget.setItem(4,r,QTableWidgetItem(str(maxField[r])))
            else:
                self.EnvWeighTableWidget.setItem(3,r,QTableWidgetItem("0"))
                self.EnvWeighTableWidget.setItem(4,r,QTableWidgetItem("0"))
        ##Economics
        criteria=[self.EcoTableWidget.verticalHeaderItem(f).text() for f in range(self.EcoTableWidget.columnCount())]
        preference=[str(self.EcoWeighTableWidget.item(2, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())]
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its name
        minField=[provider.minimumValue( f ) for f in fids]
        maxField=[provider.maximumValue( f ) for f in fids]
        for r in range(len(preference)):
            if preference[r]=='gain':
                self.EcoWeighTableWidget.setItem(3,r,QTableWidgetItem(str(maxField[r])))
                self.EcoWeighTableWidget.setItem(4,r,QTableWidgetItem(str(minField[r])))
            elif preference[r]=='cost':
                self.EcoWeighTableWidget.setItem(3,r,QTableWidgetItem(str(minField[r])))
                self.EcoWeighTableWidget.setItem(4,r,QTableWidgetItem(str(maxField[r])))
            else:
                self.EcoWeighTableWidget.setItem(3,r,QTableWidgetItem("0"))
                self.EcoWeighTableWidget.setItem(4,r,QTableWidgetItem("0"))
        ##Social
        criteria=[self.SocTableWidget.verticalHeaderItem(f).text() for f in range(self.SocTableWidget.columnCount())]
        preference=[str(self.SocWeighTableWidget.item(2, c).text()) for c in range(self.SocWeighTableWidget.columnCount())]
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its name
        minField=[provider.minimumValue( f ) for f in fids]
        maxField=[provider.maximumValue( f ) for f in fids]
        for r in range(len(preference)):
            if preference[r]=='gain':
                self.SocWeighTableWidget.setItem(3,r,QTableWidgetItem(str(maxField[r])))
                self.SocWeighTableWidget.setItem(4,r,QTableWidgetItem(str(minField[r])))
            elif preference[r]=='cost':
                self.SocWeighTableWidget.setItem(3,r,QTableWidgetItem(str(minField[r])))
                self.SocWeighTableWidget.setItem(4,r,QTableWidgetItem(str(maxField[r])))
            else:
                self.SocWeighTableWidget.setItem(3,r,QTableWidgetItem("0"))
            


    def AddField(self):
        """Add field to table in GUI"""
        if self.toolBox.currentIndex()==1:
            f=self.EnvlistFieldsCBox.currentText()
            self.EnvTableWidget.insertColumn(self.EnvTableWidget.columnCount())
            self.EnvTableWidget.insertRow(self.EnvTableWidget.rowCount())
            self.EnvTableWidget.setHorizontalHeaderItem((self.EnvTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.EnvTableWidget.setVerticalHeaderItem((self.EnvTableWidget.rowCount()-1),QTableWidgetItem(f))
            ##############
            self.EnvWeighTableWidget.insertColumn(self.EnvWeighTableWidget.columnCount())
            self.EnvWeighTableWidget.setHorizontalHeaderItem((self.EnvWeighTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.EnvWeighTableWidget.setItem(1,(self.EnvWeighTableWidget.columnCount()-1),QTableWidgetItem("1.0"))
            self.EnvWeighTableWidget.setItem(2,(self.EnvWeighTableWidget.columnCount()-1),QTableWidgetItem("gain"))

        elif self.toolBox.currentIndex()==2:
            f=self.EcolistFieldsCBox.currentText()
            self.EcoTableWidget.insertColumn(self.EcoTableWidget.columnCount())
            self.EcoTableWidget.insertRow(self.EcoTableWidget.rowCount())
            self.EcoTableWidget.setHorizontalHeaderItem((self.EcoTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.EcoTableWidget.setVerticalHeaderItem((self.EcoTableWidget.rowCount()-1),QTableWidgetItem(f))
            ##############
            self.EcoWeighTableWidget.insertColumn(self.EcoWeighTableWidget.columnCount())
            self.EcoWeighTableWidget.setHorizontalHeaderItem((self.EcoWeighTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.EcoWeighTableWidget.setItem(1,(self.EcoWeighTableWidget.columnCount()-1),QTableWidgetItem("1.0"))
            self.EcoWeighTableWidget.setItem(2,(self.EcoWeighTableWidget.columnCount()-1),QTableWidgetItem("gain"))

        elif self.toolBox.currentIndex()==3:
            f=self.SoclistFieldsCBox.currentText()
            self.SocTableWidget.insertColumn(self.SocTableWidget.columnCount())
            self.SocTableWidget.insertRow(self.SocTableWidget.rowCount())
            self.SocTableWidget.setHorizontalHeaderItem((self.SocTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.SocTableWidget.setVerticalHeaderItem((self.SocTableWidget.rowCount()-1),QTableWidgetItem(f))
            ##############
            self.SocWeighTableWidget.insertColumn(self.SocWeighTableWidget.columnCount())
            self.SocWeighTableWidget.setHorizontalHeaderItem((self.SocWeighTableWidget.columnCount()-1),QTableWidgetItem(f))
            self.SocWeighTableWidget.setItem(1,(self.SocWeighTableWidget.columnCount()-1),QTableWidgetItem("1.0"))
            self.SocWeighTableWidget.setItem(2,(self.SocWeighTableWidget.columnCount()-1),QTableWidgetItem("gain"))
        else:
            pass
        return 0


    def RemoveField(self):
        """Remove field in table in GUI"""
        if self.toolBox.currentIndex()==1:
            f=self.EnvlistFieldsCBox.currentText()
            i=self.EnvTableWidget.currentColumn()
            j=self.EnvWeighTableWidget.currentColumn()
            if i == -1 and j== -1:
                QMessageBox.warning(self.iface.mainWindow(), "geoUmbriaSUIT",
                ("column or row must be selected"), QMessageBox.Ok, QMessageBox.Ok)
            elif i != -1:
                self.EnvTableWidget.removeColumn(i)
                self.EnvTableWidget.removeRow(i)
                self.EnvWeighTableWidget.removeColumn(i)
            elif j != -1:
                self.EnvTableWidget.removeColumn(j)
                self.EnvTableWidget.removeRow(j)
                self.EnvWeighTableWidget.removeColumn(j)
        elif self.toolBox.currentIndex()==2:
            self.EcolistFieldsCBox.currentText()
            i=self.EcoTableWidget.currentColumn()
            j=self.EcoWeighTableWidget.currentColumn()
            if i == -1 and j== -1:
                QMessageBox.warning(self.iface.mainWindow(), "geoUmbriaSUIT",
                ("column or row must be selected"), QMessageBox.Ok, QMessageBox.Ok)
            elif i != -1:
                self.EcoTableWidget.removeColumn(i)
                self.EcoTableWidget.removeRow(i)
                self.EcoWeighTableWidget.removeColumn(i)
            elif j != -1:
                self.EcoTableWidget.removeColumn(j)
                self.EcoTableWidget.removeRow(j)
                self.EcoWeighTableWidget.removeColumn(j)
        elif self.toolBox.currentIndex()==3:
            self.SoclistFieldsCBox.currentText()
            i=self.SocTableWidget.currentColumn()
            j=self.SocWeighTableWidget.currentColumn()
            if i == -1 and j== -1:
                QMessageBox.warning(self.iface.mainWindow(), "geoUmbriaSUIT",
                ("column or row must be selected"), QMessageBox.Ok, QMessageBox.Ok)
            elif i != -1:
                self.SocTableWidget.removeColumn(i)
                self.SocTableWidget.removeRow(i)
                self.SocWeighTableWidget.removeColumn(i)
            elif j != -1:
                self.SocTableWidget.removeColumn(j)
                self.SocTableWidget.removeRow(j)
                self.SocWeighTableWidget.removeColumn(j)
        else:
            pass
        return 0


    def CompleteMatrix(self):
        """Autocomplete matrix of  pairwise comparison"""
        try:
            if self.toolBox.currentIndex()==1:
                cell=self.EnvTableWidget.currentItem()
                if cell.text()!=None and type(float(cell.text())==float):
                    val=round(float(cell.text())**(-1),2)
                    self.EnvTableWidget.setItem(cell.column(),cell.row(),QTableWidgetItem(str(val)))
            elif self.toolBox.currentIndex()==2:
                cell=self.EcoTableWidget.currentItem()
                if cell.text()!=None and type(float(cell.text())==float):
                    val=round(float(cell.text())**(-1),2)
                    self.EcoTableWidget.setItem(cell.column(),cell.row(),QTableWidgetItem(str(val)))
            elif self.toolBox.currentIndex()==3:
                cell=self.SocTableWidget.currentItem()
                if cell.text()!=None and type(float(cell.text())==float):
                    val=round(float(cell.text())**(-1),2)
                    self.SocTableWidget.setItem(cell.column(),cell.row(),QTableWidgetItem(str(val)))
            return 0
        except ValueError:
            QMessageBox.warning(self.iface.mainWindow(), "geoUmbriaSUIT",
            ("Input error\n" "Please insert numeric value "\
            "active"), QMessageBox.Ok, QMessageBox.Ok)


    def ChangeValue(self):
        """Event for change gain/cost"""
        if self.toolBox.currentIndex()==1:
            cell=self.EnvWeighTableWidget.currentItem()
            r=cell.row()
            c=cell.column()
            first=self.EnvWeighTableWidget.item(3, c).text()
            second=self.EnvWeighTableWidget.item(4, c).text()
            if cell.row()==2:
                val=cell.text()
                if val=="cost":
                    self.EnvWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("gain"))
                elif val=="gain":
                    self.EnvWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("cost"))
                else:
                    self.EnvWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem(str(val)))
                self.EnvWeighTableWidget.setItem(3,c, QTableWidgetItem(second))
                self.EnvWeighTableWidget.setItem(4,c, QTableWidgetItem(first))
        elif self.toolBox.currentIndex()==2:
            cell=self.EcoWeighTableWidget.currentItem()
            r=cell.row()
            c=cell.column()
            first=self.EcoWeighTableWidget.item(3, c).text()
            second=self.EcoWeighTableWidget.item(4, c).text()
            if cell.row()==2:
                val=cell.text()
                if val=="cost":
                    self.EcoWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("gain"))
                elif val=="gain":
                    self.EcoWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("cost"))
                else:
                    self.EcoWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem(str(val)))
                self.EcoWeighTableWidget.setItem(3,c, QTableWidgetItem(second))
                self.EcoWeighTableWidget.setItem(4,c, QTableWidgetItem(first))
        elif self.toolBox.currentIndex()==3:
            cell=self.SocWeighTableWidget.currentItem()
            c=cell.column()
            first=self.SocWeighTableWidget.item(3, c).text()
            second=self.SocWeighTableWidget.item(4, c).text()
            if cell.row()==2:
                val=cell.text()
                if val=="cost":
                    self.SocWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("gain"))
                elif val=="gain":
                    self.SocWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem("cost"))
                else:
                    self.SocWeighTableWidget.setItem(cell.row(),cell.column(),QTableWidgetItem(str(val)))
                self.SocWeighTableWidget.setItem(3,c, QTableWidgetItem(second))
                self.SocWeighTableWidget.setItem(4,c, QTableWidgetItem(first))
        else:
            pass
            
    def Elaborate(self):
        self.StandardizationIdealPoint()
        self.RelativeCloseness()
        self.OveralValue()
        return 0
#############################################################################################################

    def calculateWeight(self,pairwise):
        "Define vector of weight based on eigenvector and eigenvalues"
        pairwise=np.array(pairwise)
        eigenvalues, eigenvector=np.linalg.eig(pairwise)
        maxindex=np.argmax(eigenvalues)
        eigenvalues=np.float32(eigenvalues)
        eigenvector=np.float32(eigenvector)
        weight=eigenvector[:, maxindex] #extract vector from eigenvector with max vaue in eigenvalues
        weight.tolist() #convert array(numpy)  to vector
        weight=[ w/sum(weight) for w in weight ]
        if self.toolBox.currentIndex()==1:
            for i in range(len(weight)):
                self.EnvWeighTableWidget.setItem(1,i,QTableWidgetItem(str(round(weight[i],2))))
        elif self.toolBox.currentIndex()==2:
            for i in range(len(weight)):
                self.EcoWeighTableWidget.setItem(1,i,QTableWidgetItem(str(round(weight[i],2))))
        elif self.toolBox.currentIndex()==3:
            for i in range(len(weight)):
                self.SocWeighTableWidget.setItem(1,i,QTableWidgetItem(str(round(weight[i],2))))
        else:
            pass
        return weight, eigenvalues,  eigenvector


    def Consistency(self,weight,eigenvalues):
        "Calculete Consistency index in accord with Saaty (1977)"
        try:
            RI=[0.00, 0.00, 0.00,0.52,0.90,1.12,1.24,1.32,1.41]     #order of matrix: 0,1,2,3,4,5,6,7,8
            order=len(weight)
            CI=(np.max(eigenvalues)-order)/(order-1)
            return CI/RI[order-1]
        except:
            return 1.41

    def AnalyticHierarchyProcess(self):
        """Calculate weight from matrix of pairwise comparison """
        if self.toolBox.currentIndex()==1:
            criteria=[self.EnvTableWidget.verticalHeaderItem(f).text() for f in range(self.EnvTableWidget.columnCount())]
            pairwise=[[float(self.EnvTableWidget.item(r, c).text()) for r in range(len(criteria))] for c in range(len(criteria))]
        elif self.toolBox.currentIndex()==2:
            criteria=[self.EcoTableWidget.verticalHeaderItem(f).text() for f in range(self.EcoTableWidget.columnCount())]
            pairwise=[[float(self.EcoTableWidget.item(r, c).text()) for r in range(len(criteria))] for c in range(len(criteria))]
        elif self.toolBox.currentIndex()==3:
            criteria=[self.SocTableWidget.verticalHeaderItem(f).text() for f in range(self.SocTableWidget.columnCount())]
            pairwise=[[float(self.SocTableWidget.item(r, c).text()) for r in range(len(criteria))] for c in range(len(criteria))]
        else:
            pass
        weight, eigenvalues, eigenvector=self.calculateWeight(pairwise)
        consistency=self.Consistency(weight,eigenvalues)
        self.ReportLog(eigenvalues,eigenvector, weight, consistency)
        return 0

    def ReportLog(self, eigenvalues,eigenvector, weight, consistency):
        "Make a log output"
        if self.toolBox.currentIndex()==1:
            log=" Weights: %s \n Consistency: %s" % (str([round(w,2) for w in weight]),consistency)
            self.EnvTEdit.setText(log)
        elif self.toolBox.currentIndex()==2:
            log=" Weights: %s \n Consistency: %s" % (str([round(w,2) for w in weight]),consistency)
            self.EcoTEdit.setText(log)
        elif self.toolBox.currentIndex()==3:
            log=" Weights: %s \n Consistency: %s" % (str([round(w,2) for w in weight]),consistency)
            self.SocTEdit.setText(log)
        else:
            pass
        return 0


    def AddDecisionField(self,layer,Label):
        """Add field on attribute table"""
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.AddAttributes:
            res = layer.dataProvider().addAttributes( [QgsField(Label, QVariant.Double) ] )
        return 0


###########################################################################################
    def ExtractFieldSumSquare(self,field):
        """Retrive single field value from attributes table"""
        provider=self.base_Layer.dataProvider()
        fid=provider.fieldNameIndex(field)
        listValue=[]
        for feat in self.base_Layer.getFeatures():
            attribute=feat.attributes()[fid]
            listValue.append(attribute)
        listValue=[pow(l,2) for l in listValue]
        return (sum(listValue)**(0.5))
    
    def StandardizationIdealPoint(self):
        if self.toolBox.currentIndex()==1:
            criteria=[self.EnvTableWidget.verticalHeaderItem(f).text() for f in range(self.EnvTableWidget.columnCount())]
            #preference=[str(self.EnvWeighTableWidget.item(2, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())]
            weight=[float(self.EnvWeighTableWidget.item(1, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())]
            weight=[ w/sum(weight) for w in weight ]
            self.EnvGetWeightBtn.setEnabled(False)
        elif self.toolBox.currentIndex()==2:
            criteria=[self.EcoTableWidget.verticalHeaderItem(f).text() for f in range(self.EcoTableWidget.columnCount())]
            #preference=[str(self.EcoWeighTableWidget.item(2, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())]
            weight=[float(self.EcoWeighTableWidget.item(1, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())]
            weight=[ w/sum(weight) for w in weight ]
            self.EcoGetWeightBtn.setEnabled(False)
        elif self.toolBox.currentIndex()==3:
            criteria=[self.SocTableWidget.verticalHeaderItem(f).text() for f in range(self.SocTableWidget.columnCount())]
            #preference=[str(self.SocWeighTableWidget.item(2, c).text()) for c in range(self.SocWeighTableWidget.columnCount())]
            weight=[float(self.SocWeighTableWidget.item(1, c).text()) for c in range(self.SocWeighTableWidget.columnCount())]
            weight=[ w/sum(weight) for w in weight ]
            self.SocGetWeightBtn.setEnabled(False)
        else:
            pass
        provider=self.active_layer.dataProvider()
        feat = QgsFeature()
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its name
        #self.EnvTEdit.append(str(dict(zip(fids,[(field) for field in criteria]))))
        sumSquareColumn=dict(zip(fids,[self.ExtractFieldSumSquare(field) for field in criteria]))
        #provider.select(fids)
        self.active_layer.startEditing()
        for f,w in zip(fids,weight): #N.B. verifica corretto allineamento con i pesi
            for feat in self.active_layer.getFeatures():
                attributes=feat.attributes()[f]
                value=(float(attributes)/float(sumSquareColumn[f]))*w   # TOPSIS algorithm: STEP 1 and STEP 2
                #self.EnvTEdit.append(str(attributes)+"-"+str(value))
                self.active_layer.changeAttributeValue(feat.id(),f,round(value,4))
        self.active_layer.commitChanges()
        return 0
        
            
    def RelativeCloseness(self):
        """ Calculate Environmental and Socio-Economicos distance from ideal point"""
        if self.toolBox.currentIndex()==1:
            criteria=[self.EnvTableWidget.verticalHeaderItem(f).text() for f in range(self.EnvTableWidget.columnCount())]
            idealPoint=[float(self.EnvWeighTableWidget.item(3, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())]
            sumSquareColumnList=[self.ExtractFieldSumSquare(field) for field in criteria]
            idealPoint=[float(self.EnvWeighTableWidget.item(3, c).text())/sumSquareColumnList[c] \
                for c in range(self.EnvWeighTableWidget.columnCount())]
            worstPoint=[float(self.EnvWeighTableWidget.item(4, c).text())/sumSquareColumnList[c] \
                for c in range(self.EnvWeighTableWidget.columnCount())]
            provider=self.active_layer.dataProvider()
            if provider.fieldNameIndex("EnvIdeal")==-1:
                self.AddDecisionField(self.active_layer,"EnvIdeal")
            fldValue = provider.fieldNameIndex("EnvIdeal") #obtain classify field index from its name
            self.EnvTEdit.append("done") #   setText
        elif self.toolBox.currentIndex()==2:
            criteria=[self.EcoTableWidget.verticalHeaderItem(f).text() for f in range(self.EcoTableWidget.columnCount())]
            sumSquareColumnList=[self.ExtractFieldSumSquare(field) for field in criteria]
            idealPoint=[float(self.EcoWeighTableWidget.item(3, c).text())/sumSquareColumnList[c] \
                for c in range(self.EcoWeighTableWidget.columnCount())]
            worstPoint=[float(self.EcoWeighTableWidget.item(4, c).text())/sumSquareColumnList[c] \
                for c in range(self.EcoWeighTableWidget.columnCount())]
            provider=self.active_layer.dataProvider()
            if provider.fieldNameIndex("EcoIdeal")==-1:
                self.AddDecisionField(self.active_layer,"EcoIdeal")
            fldValue = provider.fieldNameIndex("EcoIdeal") #obtain classify field index from its name
            self.EcoTEdit.append("done")
        elif self.toolBox.currentIndex()==3:
            criteria=[self.SocTableWidget.verticalHeaderItem(f).text() for f in range(self.SocTableWidget.columnCount())]
            sumSquareColumnList=[self.ExtractFieldSumSquare(field) for field in criteria]
            idealPoint=[float(self.SocWeighTableWidget.item(3, c).text())/sumSquareColumnList[c] \
                for c in range(self.SocWeighTableWidget.columnCount())]
            worstPoint=[float(self.SocWeighTableWidget.item(4, c).text())/sumSquareColumnList[c] \
                for c in range(self.SocWeighTableWidget.columnCount())]
            provider=self.active_layer.dataProvider()
            if provider.fieldNameIndex("SocIdeal")==-1:
                self.AddDecisionField(self.active_layer,"SocIdeal")
            fldValue = provider.fieldNameIndex("SocIdeal") #obtain classify field index from its name
            self.SocTEdit.append("done")
        else:
            pass
        #self.EnvTEdit.append(str(idealPoint)+"#"+str(worstPoint))
        features=provider.featureCount() #Number of features in the layer.
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its name
        self.active_layer.startEditing()
        self.EnvProgressBar.setRange(1,features)
        self.EcoProgressBar.setRange(1,features)
        self.SocProgressBar.setRange(1,features)
        progress=0
        for feat in self.active_layer.getFeatures():
            IP=WP=0
            for f,idp,wrp in zip(fids,idealPoint,worstPoint):
                progress=progress+1
                attributes = feat.attributes()
                IP =IP+(float(attributes[f]-idp)**2)   # TOPSIS algorithm: STEP 4
                WP =WP+(float(attributes[f]-wrp)**2)
            relativeCloseness=(WP**(0.5))/((WP**(0.5))+(IP**(0.5))) 
            self.active_layer.changeAttributeValue(feat.id(), fldValue, round(float(relativeCloseness),4))
            self.EnvProgressBar.setValue(progress)
            self.EcoProgressBar.setValue(progress)
            self.SocProgressBar.setValue(progress)
        self.active_layer.commitChanges()
        self.EnvProgressBar.setValue(1)
        self.EcoProgressBar.setValue(1)
        self.SocProgressBar.setValue(1)
        return 0

        
    def OveralValue(self):
        """Sum Environmental and Socio-economics value for calculate  Sustainable value"""
        provider=self.active_layer.dataProvider()
        if provider.fieldNameIndex("SustIdeal")==-1:
            self.AddDecisionField(self.active_layer,"SustIdeal")
        fldValue = provider.fieldNameIndex("SustIdeal") #obtain classify field index from its name
        fids=[provider.fieldNameIndex(c) for c in ['EnvIdeal','EcoIdeal','SocIdeal']]
        if -1 not in fids:
            self.active_layer.startEditing()
            for feat in self.active_layer.getFeatures():
                attributes=feat.attributes()
                #self.EnvTEdit.append(str(fids)+"-"+str([(attributes[att]) for att in fids]))
                value=sum([float(str(attributes[att])) for att in fids])
                self.active_layer.changeAttributeValue(feat.id(), fldValue, round(float(value),4))
            self.active_layer.commitChanges()
            return 0
        else:
            return -1
        


###########################################################################################

    def Symbolize(self,field):
        """Prepare legends for environmental, socio economics and sustainable values"""
        classes=['very low (molto basso)', 'low (basso)','medium (medio)','high (alto)','very high (molto alto)']
        fieldName = field
        numberOfClasses=len(classes)
        layer = self.iface.activeLayer()
        fieldIndex = layer.fieldNameIndex(fieldName)
        provider = layer.dataProvider()
        minimum = provider.minimumValue( fieldIndex )
        maximum = provider.maximumValue( fieldIndex )
        RangeList = []
        Opacity = 1
        for c,i in zip(classes,range(len(classes))):
        # Crea il simbolo ed il range...
            Min = minimum + (( maximum - minimum ) / numberOfClasses * i)
            Max = minimum + (( maximum - minimum ) / numberOfClasses * ( i + 1 ))
            Label = "%s [%.2f - %.2f]" % (c,Min,Max)
            if field=='SustIdeal':
                Colour = QColor(255-255*i/numberOfClasses,255*i/numberOfClasses,0) #red to green
            elif field=='EnvIdeal':
                Colour = QColor(255-255*i/numberOfClasses,255,125-125*i/numberOfClasses) #yellow to green
            elif field=='EcoIdeal':
                Colour = QColor(255,255-255*i/numberOfClasses,0) #yellow to red
            elif field=='SocIdeal':
                Colour = QColor((255-100*i/numberOfClasses),255,204+51*i/numberOfClasses) #yellow to cyan 204,255,255
            Symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
            Symbol.setColor(Colour)
            Symbol.setAlpha(Opacity)
            Range = QgsRendererRangeV2(Min,Max,Symbol,Label)
            RangeList.append(Range)
        Renderer = QgsGraduatedSymbolRendererV2('', RangeList)
        Renderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
        Renderer.setClassAttribute(fieldName)
        add=QgsVectorLayer(layer.source(),field,'ogr')
        add.setRendererV2(Renderer)
        QgsMapLayerRegistry.instance().addMapLayer(add)

    def RenderLayer(self):
        """ Load thematic layers in canvas """
        layer = self.iface.activeLayer()
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        #layer = QgsVectorLayer(self.OutlEdt.text(), "geosustainability", "ogr")
        layer = QgsVectorLayer(self.OutlEdt.text(), (os.path.basename(str(self.OutlEdt.text()))), "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        fields=['EnvIdeal','EcoIdeal','SocIdeal','SustIdeal']
        for f in fields:
            self.Symbolize(f)

###########################################################################################
    def RefreshLayer(self):
        self.active_layer.setCacheImage( None )
        self.active_layer.triggerRepaint()
        self.EnvTEdit.append("refresced")
    
    def ExtractAttributeValue(self,field):
        """Retrive single field value from attributes table"""
        fields=self.active_layer.pendingFields()
        provider=self.active_layer.dataProvider()
        fid=provider.fieldNameIndex(field)
        listValue=[]
        if fields[fid].typeName()=='Real' or fields[fid].typeName()=='Integer':
            for feat in self.active_layer.getFeatures():
                attribute=feat.attributes()[fid]
                listValue.append(float(attribute))
        else:
            for feat in self.active_layer.getFeatures():
                attribute=feat.attributes()[fid]
                listValue.append(str(attribute))
        return listValue

    def BuildOutput(self):
        """General function for all graphical and tabula output"""
        currentDir = unicode(os.path.abspath( os.path.dirname(__file__)))
        self.BuildGraphPnt(currentDir)
        self.BuildGraphIstogram(currentDir)
        self.BuildHTML()
        webbrowser.open(os.path.join(currentDir,"barGraph.html"))
        return 0

    def BuildGraphPnt(self,currentDir ):
        """ Build points graph using pyplot"""
        fig = plt.figure()
        #fig.subplots_adjust(bottom=0.2)
        ax = fig.add_subplot(111)
        if os.path.isfile(os.path.join(currentDir,"points.png"))==True:
            os.remove(os.path.join(currentDir,"points.png"))
        y=self.ExtractAttributeValue('EnvIdeal')
        x1=self.ExtractAttributeValue('EcoIdeal')
        x2=self.ExtractAttributeValue('SocIdeal')
        x=[i+j for i,j in zip(x1,x2)]
        label=self.LabelListFieldsCBox.currentText()
        labels=self.ExtractAttributeValue(label)
        plt.ylabel('Envirnmental value')
        plt.xlabel('Socio-economic value')
        g=plt.plot(x,y,'ro')

        plt.setp(g, 'markersize', 5)
        plt.setp(g, 'markerfacecolor', 'g')
        for i in range(len(labels)):
            plt.text (x[i], y[i], labels[i], fontsize=6)
        ########################################
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        im = plt.imread(os.path.join(currentDir,"base.png"))
        implot = plt.imshow(im,zorder=0, extent=[xlim[0], xlim[1],  ylim[0], ylim[1]])
        ########################################
        plt.savefig(os.path.join(currentDir,"points.png"))
        plt.close('all')
        return 0


    def BuildGraphIstogram(self,currentDir):
        """Build Istogram graph using pyplot"""
        if os.path.isfile(os.path.join(currentDir,"histogram.png"))==True:
            os.remove(os.path.join(currentDir,"histogram.png"))
        EnvValue=self.ExtractAttributeValue('EnvIdeal')
        EcoValue=self.ExtractAttributeValue('EcoIdeal')
        SocValue=self.ExtractAttributeValue('SocIdeal')
        SuitValue=[x+y+z for (x,y,z) in zip(EnvValue,EcoValue,SocValue)]
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.2)
        fig.subplots_adjust()
        ax = fig.add_subplot(111)
        ax.margins(0.05, None)
        xpos = np.arange(len(SuitValue))    # the x locations for the groups
        width = 0.8     # the width of the bars: can also be len(x) sequence
        label=self.LabelListFieldsCBox.currentText()
        labels=self.ExtractAttributeValue(label)
        p1 = plt.bar((xpos), EnvValue, width=width, color='g',align='center') # yerr=womenStd)
        p2 = plt.bar((xpos), EcoValue, width=width, color='r', bottom=EnvValue, align='center') #, yerr=menStd)
        bot=[e+c for e,c in zip(EnvValue,EcoValue)]
        p3 = plt.bar((xpos), SocValue, width=width, color='c', bottom=bot, align='center') #, yerr=menStd)
        #n, bins, patches = plt.hist( [EnvValue,EcoValue,SocValue], histtype='bar', stacked=True)
        plt.ylabel('Scores')
        plt.title('Sustainability')
        plt.xticks((xpos), tuple(labels),rotation=90,fontsize=6 )
        plt.legend((p1[0], p2[0], p3[0]), ('Environment', 'Economics','Social'))
        plt.savefig(os.path.join(currentDir,"histogram.png"))
        self.LblGraphic.setPixmap(QtGui.QPixmap(os.path.join(currentDir,"histogram.png")))
        plt.close('all')
        return 0
        
    def BuildHTML(self):
        EnvValue=self.ExtractAttributeValue('EnvIdeal')
        EcoValue=self.ExtractAttributeValue('EcoIdeal')
        SocValue=self.ExtractAttributeValue('SocIdeal')
        SuitValue=[x+y+z for (x,y,z) in zip(EnvValue,EcoValue,SocValue)]
        label=self.LabelListFieldsCBox.currentText()
        labels=self.ExtractAttributeValue(label)
        labels=[str(l) for l in labels]
        htmlGraph.BuilHTMLGraph(SuitValue,EnvValue,EcoValue,SocValue,labels)
        return 0
        
        
        
###################################################################################################
    def SaveCfg(self):
        #pathSource=os.path.dirname(str(self.base_Layer.source()))
        currentDIR = unicode(os.path.dirname(str(self.base_Layer.source())))
        fileCfg = open(currentDIR+"\\setting.csv","w")
        label=[str(self.EnvWeighTableWidget.item(0, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())] +\
            [str(self.EcoWeighTableWidget.item(0, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())] + \
            [str(self.SocWeighTableWidget.item(0, c).text()) for c in range(self.SocWeighTableWidget.columnCount())]
        criteria,preference,weight=self.UsedCriteria()
        for l in label:
            fileCfg.write(str(l)+";")
        fileCfg.write("\n")
        for c in criteria:
            fileCfg.write(str(c)+";")
        fileCfg.write("\n")
        fileCfg.write(";".join(weight))
        fileCfg.write("\n")
        for p in preference:
            fileCfg.write(str(p)+";")
        fileCfg.close()
        
        
    def about(self):
        """    Visualize an About window."""
        QMessageBox.about(self, "About geoSustainability",
        """
            <p>geoUmbriaSUIT version 2.0<br />2013-05-1<br />License: GPL v. 3</p>
            <p>Università degli Studi di Perugia - Dipartimento di Scienze Economiche, Estimative e degli Alimenti, <a href="http://www.unipg.it">www.unipg.it</a></p>
            <p>Agenzia Regionale per la Protezione Ambientale - ARPA, <a href="http://www.arpa.umbria.it">www.arpa.umbria.it</a></p>
            <p>Description</p>
             <p>Please report any bug to <a href="mailto:g_massa@libero.it">g_massa@libero.it</a></p>
        """)

    def open_help(self):
        currentDir = unicode(os.path.abspath( os.path.dirname(__file__)))
        webbrowser.open(os.path.join(currentDir,"data.html"))


###################################################################################################

    def DiscretizeDecision(self,value,listClass,numberOfClasses):
        DiscValue=-1
        for o,t in zip(range(numberOfClasses),range(1,numberOfClasses+1)) :
            if ((float(value)>=float(listClass[o])) and (float(value)<=float(listClass[t]))):
                DiscValue=o+1
        return DiscValue
    
    def AddDiscretizedField(self):
        """add new field"""
        numberOfClasses=5
        provider=self.base_Layer.dataProvider()
        #provider=self.active_layer.dataProvider()
        if provider.fieldNameIndex("Classified")==-1:
            self.AddDecisionField(self.base_Layer,"Classified")
        fidClass = provider.fieldNameIndex("Classified") #obtain classify field index from its name
        listInput=self.ExtractAttributeValue("SustIdeal")
        widthOfClass=(max(listInput)-min(listInput))/numberOfClasses
        listClass=[(min(listInput)+(widthOfClass)*i) for i in range(numberOfClasses+1)]
        #self.EnvTEdit.setText(str(listClass))
        self.base_Layer.startEditing()
        decision=[]
        for feat in self.base_Layer.getFeatures():
            DiscValue=self.DiscretizeDecision(listInput[int(feat.id())],listClass,numberOfClasses)
            self.base_Layer.changeAttributeValue(feat.id(), fidClass, float(DiscValue))
        decision.append(DiscValue)
        self.base_Layer.commitChanges()
        return list(set(decision))

    def UsedCriteria(self):
        criteria=[self.EnvTableWidget.verticalHeaderItem(f).text() for f in range(self.EnvTableWidget.columnCount())] + \
            [self.EcoTableWidget.verticalHeaderItem(f).text() for f in range(self.EcoTableWidget.columnCount())] + \
            [self.SocTableWidget.verticalHeaderItem(f).text() for f in range(self.SocTableWidget.columnCount())]
        weight=[str(self.EnvWeighTableWidget.item(1, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())] +\
            [str(self.EcoWeighTableWidget.item(1, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())] + \
            [str(self.SocWeighTableWidget.item(1, c).text()) for c in range(self.SocWeighTableWidget.columnCount())]
        preference=[str(self.EnvWeighTableWidget.item(2, c).text()) for c in range(self.EnvWeighTableWidget.columnCount())] +\
            [str(self.EcoWeighTableWidget.item(2, c).text()) for c in range(self.EcoWeighTableWidget.columnCount())] + \
            [str(self.SocWeighTableWidget.item(2, c).text()) for c in range(self.SocWeighTableWidget.columnCount())] 
        return criteria, preference,weight
        
    def WriteISFfile(self,decision):
        currentDIR = unicode(os.path.abspath( os.path.dirname(__file__)))
        out_file = open(currentDIR+"\\example.isf","w")
        criteria,preference,weight=self.UsedCriteria()
        criteria.append("Classified")
        preference.append("gain")
        #decision=list(set(self.ExtractAttributeValue("Classified")))
        decision=[int(i) for i in decision]
        out_file.write("**ATTRIBUTES\n") 
        for c in (criteria):
            if(str(c)=="Classified"):
                out_file.write("+ Classified: %s\n"  % (decision))
            else:
                out_file.write("+ %s: (continuous)\n"  % (c))
        out_file.write("decision: Classified")
        out_file.write("\n\n**PREFERENCES\n")
        for c,p in zip(criteria,preference):
            out_file.write("%s: %s\n"  % (c,p))
        out_file.write("\n**EXAMPLES\n")
        provider=self.base_Layer.dataProvider()
        fids=[provider.fieldNameIndex(c) for c in criteria]  #obtain array fields index from its names
        for feat in self.base_Layer.getFeatures():
            attribute = [feat.attributes()[j] for j in fids]
            for i in (attribute):
                out_file.write(" %s " % (i))
            out_file.write("\n")
        out_file.write("\n**END")
        out_file.close()
        return 0

    def SelectFeatures(self):
        self.selection_layer = self.iface.activeLayer()
        itemSelect=self.RulesListWidget.currentItem().text()
        itemSelect=str(itemSelect.split("\t")[1])
        itemSelect=itemSelect.replace('[','')
        itemSelect=itemSelect.replace(']','')
        itemSelect=map(int,itemSelect.split(','))
        itemSelect=[(cod-1) for cod in itemSelect]
        self.selection_layer.setSelectedFeatures(itemSelect)
        self.EnvTEdit.append(str(itemSelect))
        return 0

    def ShowRules(self):
        currentDIR = unicode(os.path.abspath( os.path.dirname(__file__)))
        rules=open(currentDIR+"\\rules.rls")
        R=rules.readlines()
        self.RulesListWidget.clear()
        for E in R:
            self.RulesListWidget.addItem(E)
        self.RulesListWidget.itemClicked.connect(self.SelectFeatures)
        return 0

    def ExtractRules(self):
        pathSource=os.path.dirname(str(self.iface.activeLayer().source()))
        decision=self.AddDiscretizedField()
        self.WriteISFfile(decision)
        DOMLEM.main(pathSource)
        self.ShowRules()
        return 0




