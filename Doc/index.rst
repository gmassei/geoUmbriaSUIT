.. geoUmbriaSUIT documentation master file, created by
   sphinx-quickstart on Sun Feb 02 22:41:59 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

   
Welcome to geoUmbriaSUIT's documentation!
=========================================

Geographical MCDA for sustainability assessment


Index
-----
.. toctree::
   :maxdepth: 3

   manual
   tutorial
   bibliography





Introduction
------------

	GeoUmbriaSUIT  is a QGIS plugin for sustainability assessment in geographic  environmental, using environmental,  economics and social criteria. 
	It implements the algorithm  TOPSIS **[2]** which define a ranking based on distance from  worst point and  closeness to a ideal point, for each used criteria.
	Entry of  weights can be done directly, if known, or  with the use of a pairwise comparation  table; in this way the user is led to define  a final vector weight, in a repeatable and verifiable path.
	
	The the plugin works in QGS **[3]**, a free and open source geographic software, quite widely used in several fields. With QGIS and python is quite simple extend the software functionality and build new plugin. 
	
	GeoUmbriaSUIT is hosted in official qgis plugin repository <http://plugins.qgis.org/plugins/>_ and is available under GNU GPL licence.
	The outputs of geoUmbriaSUIT are both geographic  and graphics. The first shows the maps of the multicriteria analysis results for each elementary  area. The graphic output shows the numerical value of sustainability, with the use of  bars , bubble and points.
	
	The plugin implements the DOMLEM **[4]** algorithm based on the "dominance based rough set" theory **[5]**. With its use the user can know the decisional rules derived from the TOPSIS algorithm and give a better overview of  the ranking  of sustainability shows with maps and graphs. The transparency, the  analysis and the  back analysis capability is dramatically increased.
	
	The plugin geoUmbriaSUIT use a geographic vector file, eg. a shapefile, where the graphics data shows the single evaluation units (for example countries, regions or municipalities), while the alphanumeric data  (the attribute table), describe the environmental, economics and social indicators. With the use of the algorithms available in the plugin, is possible treat separately the indicators in the three dimension of sustainability and compute three different indexes. The linear combination of the three  indexes give  a overall sustainability index for each geographic units.. 
	
	The user can use a wide number of indicators (the same number of those present in the shapefile) and he can use  a set of data prepared by himself. However, using the data supplied from ARPA Umbria granted more robustness and repeatability  of output. In the next paragraphs we'll use "plugin" and "geoUmbriaSUIT" as synonymous. 
	
	We intend for “research units”  an administrative unit described by environmental, economics and social indicators (eg.  municipality, provinces, regions, country, etc.) . 
	The numeric output of geoUmbriaSUIT is the “sustainability index”, given from the linear combination of three different indexes: environmental index, economics index and social index. Higher is the value of those  indexes and better is the performance of a single "research units".
 