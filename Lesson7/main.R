# TEAM Big Coders-Elke and Joy
# January 2017
# Import packages



library(sp)
library(rgdal)
library(rgeos)
library(raster)


# Source functions
source('R/downLoad.R')
source('R/time.R')

##Step 1. Download files and Unpack contents
downLoad('https://raw.githubusercontent.com/GeoScripting-WUR/VectorRaster/gh-pages/data/MODIS.zip',"MODIS","zip")

##Step 2. Generate brick out of the files
modisPath <- list.files("data", pattern = glob2rx('MOD*.grd'), full.names = TRUE)
nlMODIS <- brick(modisPath)
plot(nlMODIS)
nlMODIS

##Step 3. Select Municipality level data as  vector polygons
nlMuni <- getData('GADM',country='NLD', level=2)
nlMuni@data <- nlMuni@data[!is.na(nlMuni$NAME_2),] # Remove rows with NA


##Step 5. Reproject dataset
nlMuniCRS <- spTransform(nlMuni, CRS(proj4string(nlMODIS)))


##Step 6. Select time 
#Sepecify time of analysis. Write either the name of the month like this "April'or write the word "year" for the full year analysis
timeVar<-"September"
nlMODISmonth<-time(timeVar)


##Step 7. Extract Value
rvals <- extract(nlMODISmonth, nlMuniCRS,fun=mean,sp=TRUE)
head(rvals)

##Step 8. Calculate Max and assign it to the index(ID)
maxMuni<-which.max(rvals[[timeVar]])
muniID<-maxMuni

muniContour <- nlMuniCRS[nlMuniCRS$ID_2 == muniID,]


##Step 8. Plot
plot(nlMODISmonth, main=paste("Municipality is:", as.character(muniContour$NAME_2),"Time:",timeVar))
plot(rvals, add=TRUE)
plot(muniContour,lwd = 3, col="red" , add=TRUE)

spplot(rvals, zcol=timeVar, main=paste("Municipality is:", as.character(muniContour$NAME_2), Time:",timeVar))


