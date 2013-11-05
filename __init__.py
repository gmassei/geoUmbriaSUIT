# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name			 	 : geoUmbriaSUIT 2.0
Description          : geographical MCDA for sustainability assessment
Date                 : 01/04/2013
copyright            : (C) 2012 by Gianluca Massei
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


def classFactory(iface):	# inizializza il plugin
	from geoSustainability import geoSustainability	# importiamo la classe che realizza il plugin
	return geoSustainability(iface)	# creiamo una istanza del plugin
