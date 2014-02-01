# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name			 	 : Vector geoMCDA
Description          :
Date                 :
copyright            : (C) 2010 by Gianluca Massei
email                : g_massa@libero.it

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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMapLayer
# Initialize Qt resources from file resources.py
import resources
import os
import webbrowser


class geoSustainability:

	def __init__(self, iface):
		self.iface = iface	# salviamo il riferimento all'interfaccia di QGis

	def initGui(self):	# aggiunge alla GUI di QGis i pulsanti per richiamare il plugin
		# creiamo l'azione che lancerà il plugin
		self.action = QAction(QIcon(":/plugins/geosustainability/icon.png"), "geoUmbriaSUIT", self.iface.mainWindow())
		#self.action = QAction( "geoSUIT", self.iface.mainWindow() )
		QObject.connect( self.action, SIGNAL( "triggered()" ), self.run )

		# aggiunge il plugin alla toolbar
		self.iface.addToolBarIcon( self.action )
		self.iface.addPluginToMenu( "&geoUmbriaSUIT", self.action )

	def unload(self):	# rimuove dalla GUI i pulsanti aggiunti dal plugin
		self.iface.removeToolBarIcon( self.action )
		self.iface.removePluginMenu( "&geoUmbriaSUIT", self.action )

	def run(self):	# richiamato al click sull'azione
		try:
			import matplotlib.pyplot as plt
			import numpy as np
		except ImportError, e:
			QMessageBox.information(None, QCoreApplication.translate('geoUmbriaSUIT', "Plugin error"), \
			QCoreApplication.translate('geoUmbriaSUIT', "Couldn't import Python modules 'matplotlib' and 'numpy'. [Message: %s]" % e))
			return
		from geoSUIT import geoSUITDialog
		self.active_layer = self.iface.activeLayer()
		if ((self.active_layer == None) or (self.active_layer.type() != QgsMapLayer.VectorLayer)):
			QMessageBox.warning(self.iface.mainWindow(), "geoSUIT",
			("No active layer found\n" "Please make one or more vector layer " "active"), QMessageBox.Ok, QMessageBox.Ok)
			webbrowser.open("http://maplab.alwaysdata.net/geoUmbriaSUIT.html")
			return
		dlg = geoSUITDialog(self.iface)
		dlg.exec_()


