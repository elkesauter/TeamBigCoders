# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:21:04 2017

@author: ubuntu
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:30:33 2017

@author: ubuntu
"""
#Team Big Coders-Elke and Joy

#import libraries
from osgeo import ogr,osr
import os




#Verify existence of drivers
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )

if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName
    
    
#Specify shapefile and layer names
fnWUR = "data/pointsWUR.shp"
layernameWUR = "data/pointsWURL"

## Create shape file
ds = drv.CreateDataSource(fnWUR)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

## Create Layer
layer=ds.CreateLayer(layernameWUR, spatialReference, ogr.wkbPoint)
print(layer.GetExtent())

## Create a points in Wageningen
point1 = ogr.Geometry(ogr.wkbPoint)
point2 = ogr.Geometry(ogr.wkbPoint)

## SetPoint(self, int point, double x, double y, double z = 0)
point1.SetPoint(0,5.655737,51.990349) 
point2.SetPoint(0,5.665541,51.987625)

## Feature defenition from properties of the layer
layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)

## Add the points to the feature
feature1.SetGeometry(point1)
feature2.SetGeometry(point2)

## Store the feature in a layer
layer.CreateFeature(feature1)
layer.CreateFeature(feature2)
print "The new extent"
print layer.GetExtent()

ds.Destroy()

#drv is the ESRI shapefile driver from above and fnWUR the filename
ds = drv.Open(fnWUR, 1)


print "For the KML file export the following line is used in the terminal: ogr2ogr -f KML pointWURk.kml pointsWUR.shp"
!ogr2ogr -f KML data/pointWURk.kml data/pointsWUR.shp




print "For the GeoJSON file export the following line is used in the terminal: ogr2ogr -f GeoJSON -t_srs crs:84 pointsWURg.geojson pointsWUR.shp"
!ogr2ogr -f GeoJSON -t_srs crs:84 data/pointsWURg.geojson data/pointsWUR.shp


#Visualize in a map with folium package

import folium
import os
import folium
map_osm = folium.Map(location=[45.5236, -122.6750])
map_osm.save('data/osmWUR.html')

pointsGeo=os.path.join("data/pointsWURg.geojson")
map_points = folium.Map(location=[52,5.7],tiles='Mapbox Bright', zoom_start=6)
map_points.choropleth(geo_path=pointsGeo)
map_points.save('data/pointsWUR.html')

