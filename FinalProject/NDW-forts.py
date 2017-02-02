# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 14:05:19 2017

@author: ubuntu
"""

#Specify your distance threshold
distancelimit=0.5

#Please create a folder with the name specified in path and store your pictures here
path="Pics"
dirshp="Forts_point_FINAL/"

api_key=
api_secret=

#Choose your Flick Search tags
tag='Nieuwe Hollandse Waterlinie,New Dutch Waterline'


name2='FortUNESCOmapHollandseWaterlinie.html'

locationself=[52,5]

        
def shpmapping(distancelimit,path,dirshp,api_key,api_secret,name2,tag):
    ####modules########
    import os
    ######directory######
    
    directory=os.getcwd()
    print directory


    ######importing other functions######
    from mapfunctionsForts import listfeature
    from mapfunctionsForts import photomap
    from mapfunctionsForts import flickrmap
    from mapfunctionsForts import featuremap
    #### list shapefiles forts######
    lijst=listfeature(dirshp)
            
    ####### Displaying photos on map########
    lijstPC=photomap(path,locationself, directory)

    ####### Displaying flickr photos on map#########
    lijstflickr=flickrmap(api_key,api_secret,tag)

    ########Displaying fort elements with pictures within a certain radius######
    featuremap(lijst,lijstflickr,lijstPC,distancelimit,name2,locationself)







