# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 12:02:56 2017

@author: ubuntu
"""


######################SHAPEFILE#################
def listfeature(dirshp):
    import osgeo
    from osgeo import ogr
    from osgeo import osr
    from osgeo import gdal
    import os
    from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
    
    #create shapefile
    lijst=[]
    for filename in os.listdir(dirshp):
        
        #getting coordinates systems
        if filename.endswith(".shp"):
            driver = ogr.GetDriverByName("ESRI Shapefile")
            target = osr.SpatialReference()
            target.ImportFromEPSG(4326)
            source = osr.SpatialReference()
            source.ImportFromEPSG(28992)
            dataSource = driver.Open(dirshp+filename)
            layer = dataSource.GetLayer()
            
            #transform coordinates from RD New to WGS84
            for feature in layer:
                geom = feature.GetGeometryRef()
                coordinates=geom.Centroid().ExportToWkt()
                transform = osr.CoordinateTransformation(source, target)
                point = ogr.CreateGeometryFromWkt(coordinates)
                point.Transform(transform)
                pointnew= point.ExportToWkt()
                print pointnew
                lon=float(pointnew[7:21])
                lat=float(pointnew[23:38])
                lijst+=[(lat,lon)]
    return lijst
    
###############PC PHOTOS#########################  
def photomap(path,locationself, directory):
    import folium
    import os
    from pil import get_exif_data
    from pil import get_lat_lon
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    
    #create map
    map1 = folium.Map(location=locationself)
    
    #create list of PC photo paths and coordinates
    lijstPC=[]
    directoryPC=os.listdir(path)
    htmlpath="file://"+directory+"/"
    
    #check if there are photos in the Pics folder
    if len(directoryPC)==0:
        print "There are no PC photos, look for photos in flickr"
        
    #gather coordinates and create list of Picture Path and coordinates
    for filename2 in directoryPC:
        print filename2
        fullName=os.path.join(path, filename2)
        print fullName
        f = open(fullName, 'r')
        totalpath=htmlpath + str(fullName)
        print totalpath
        image = Image.open(f)# load an image through PIL's Image object
        exif_data = get_exif_data(image)
        coords= get_lat_lon(exif_data)
        
        #check for pictures without coordinates, these will be ignored
        if not None in coords:
            lati=coords[0]
            print lati
            longi=coords[1]
            lijstPC+=[(totalpath,lati,longi)]
            
            
            #create PC popups and markers
            code='<h2>PC Photo</h2><img src="'+totalpath+'" style="width:500px;height:500px;">'
            #code='<img src="'+totalpath+'" style="width:500px;height:500px;">'
            iframe = folium.element.IFrame(html=code,width=520,height=570)
            popphoto = folium.Popup(iframe,max_width=520)
            urlphoto='http://pbs.twimg.com/profile_images/1695197720/twitpic-camera-icon_reasonably_small.png'
            iconphoto = folium.features.CustomIcon(urlphoto,icon_size=(20, 20))
            folium.Marker([float(lati),float(longi)],popup=popphoto, icon = iconphoto).add_to(map1)
    return lijstPC,map1

###################FLICKR PHOTOS###############################
def flickrmap(api_key,api_secret,map1,tag,name1):
    import flickrapi
    import folium
    
    #get flickr authorization
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    token=flickr.authenticate_via_browser(perms='write')
    
    
    #create flickr photo list with url and coordinates
    lijstflickr=[]

    
    #get only flickr photos with location that match the chosen tag
    for photo in flickr.walk(tag_mode=any,tags=tag, has_geo=1,extras='url_m'):
        ID=photo.get('id')
        title=photo.get('title')
        url=photo.get('url_m')
        loc=flickr.photos.geo.getLocation(api_key=api_key,photo_id=ID)

        #gather coordinates and create list of Picture URL and coordinates
        for elem in loc.iter('location'):
            attribute= elem.attrib
            latitude=attribute.get('latitude')
            latitude=float(latitude)
            longitude=attribute.get('longitude')  
            longitude=float(longitude)
            lijstflickr+=[(url,latitude,longitude)]
            
            #create Flickr popups and markers
            urlcode=' <h2>Flickr Photo</h2><img src="'+url+'">'      
            iframe = folium.element.IFrame(html=urlcode,width=520,height=450)
            popflickr = folium.Popup(iframe,max_width=520)
            urlflickr='http://library.uitm.edu.my/v1/images/stories/flickr.png'
            iconflickr = folium.features.CustomIcon(urlflickr,
                                      icon_size=(20, 20))
            folium.Marker([latitude,longitude],popup=popflickr,icon =iconflickr).add_to(map1)

    
    return lijstflickr,map1

########################TOTAL PHOTO INTEGRATION TO FORT##########################3
def featuremap(lijst,lijstflickr,lijstPC,distancelimit,map1,name1,locationself):
    import folium
    
    from haversine import Haversine
    
    #for every fort assemble the surrounding pictures(PC Photos and Flickr) 
    #into the photo gallery of the fort displayed as a popup in HTML
    for fort in lijst:
        code="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<title>New Dutch Waterline</title>

<style type="text/css">
body {
	background: #778899;
	color: #eee;
	margin-top: 20px;
	font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
}
a {
	color: #FFF;
}
a:hover {
	color: yellow;
	text-decoration: underline;
}
.thumbnails img {
	height: 80px;
	border: 1px solid #555;
	padding: 1px;
	margin: 0 10px 10px 0;
}

.thumbnails img:hover {
	border: 1px solid #00ccff;
	cursor:pointer;
}

.preview img {
	border: 1px solid #444;
	padding: 1px;
	width: 500px;
}
</style>

</head>
<body>

<div class="gallery" align="center">
	<h2>New Dutch Waterline Fort </h2>
	

	<br />

	<div class="thumbnails">
 """ 
        #check first flickr photos within a distance threshold specified by the user
        #add the url of the flickr image to the fort popup
        count=0
        for flickrphoto in lijstflickr:
            count=count+1
            countFs=str(count)
            url,latitude,longitude=flickrphoto
            distance=Haversine(longitude,latitude,fort[1],fort[0])
            if distance <distancelimit:
                code=code + '<img onmouseover="preview.src=img'+countFs+'.src" name="img'+countFs+'" src="'+url+'" alt=""/>'
             
        #check second the PC photos within a distance threshold specified by the user
        #add the url of the PC image to the fort popup       
        for PCphoto in lijstPC:
            count=count+1
            countPCs=str(count)
            totalpathPC,lati,longi=PCphoto
            distancePC=Haversine(longi,lati,fort[1],fort[0])
            if distancePC <distancelimit:
                code=code+ '<img onmouseover="preview.src=img'+countPCs+'.src" name="img'+countPCs+'" src="'+totalpathPC+'" alt=""/>'   
        
        #complete the rest of the HTML of the fort photo gallery
        code2="""
    </div><br/>

	<div class="preview" align="center">
		<img name="preview" src="https://www.staatsbosbeheer.nl/~/media/08-dossiers/monumenten/waterlinie-logo-2016-600.jpg" alt=""/>
	</div>

</div>


</body>
</html>
 """  
        
        code=code+code2
        
        ##create fort popups and markers
        icon_url='http://www.bastis-tourism.info/images/thumb/8/83/Icon_Castle.png/50px-Icon_Castle.png'
        iconnew = folium.features.CustomIcon(icon_url,
                                          icon_size=(30, 30))
        iframe = folium.element.IFrame(html=code,width=700,height=700)
        poppin = folium.Popup(iframe,max_width=700)
        folium.Marker([fort[0],fort[1]],popup=poppin,icon = iconnew).add_to(map1)
        code="" 
    map1.save(name1)
