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

###Elke
##api_key='331df65514d37c6b051950436a9bedb8'
##api_secret='fd9494bf6e6988f5'

###JOY
api_key=
api_secret=

#Choose your Flick Search tags
tag='Nieuwe Hollandse Waterlinie,New Dutch Waterline'

name1='PhotoSourceMapHollandseWaterlinie.html'


locationself=[52,5]

        
def shpmapping(distancelimit,path,dirshp,api_key,api_secret,name1,tag):
    ####modules########
    import os
    ######directory######
    
    directory=os.getcwd()


    ######importing other functions######
    from mapfunctionsSources import listfeature
    from mapfunctionsSources import photomap
    from mapfunctionsSources import flickrmap
    from mapfunctionsSources import featuremap
    #### list shapefiles forts######
    lijst=listfeature(dirshp)
            
    ####### Displaying photos on map########
    lijstPC,map1=photomap(path,locationself, directory)

    ####### Displaying flickr photos on map#########
    lijstflickr,map1=flickrmap(api_key,api_secret,map1,tag,name1)

    ########Displaying fort elements with pictures within a certain radius######
    featuremap(lijst,lijstflickr,lijstPC,distancelimit,map1,name1,locationself)







