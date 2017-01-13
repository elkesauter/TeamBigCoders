# Elke and Joy
# January 2017
# Import packages

# Source functions
library(raster)
library(sp)
source('R/NDVI_function.R')
source('R/cloudMask.R')

##Step 1. Download files for Landsat 5 (LT5) and Landsat 8 (LC8)
library(tools)
download.file(url = 'https://www.dropbox.com/s/akb9oyye3ee92h3/LT51980241990098-SC20150107121947.tar.gz?dl=1', destfile = 'LT51980241990098-SC20150107121947.tar.gz', method = 'wget')
download.file(url = 'https://www.dropbox.com/s/i1ylsft80ox6a32/LC81970242014109-SC20141230042441.tar.gz?dl=1', destfile = 'LC81970242014109-SC20141230042441.tar.gz', method = 'wget')


##Step 2. Unpack the archive
untar('LT51980241990098-SC20150107121947.tar.gz', exdir="data")
untar('LC81970242014109-SC20141230042441.tar.gz', exdir="data")


##Step 3. Date Extraction from file name string
LT5name<-"LT51980241990098-SC20150107121947.tar.gz"
LT5year<-substr(LT5name, 10,13)
print(paste("The year of the Landsat 5 image is: ", LT5year))

LC8name<-"LC81970242014109-SC20141230042441.tar.gz"
LC8year<-substr(LC8name, 10,13)
print(paste("The year of the Landsat 8 image is: ", LC8year))


##Step 4. Create listand then convert to stacks

listLT5<-list.files('data/', pattern = glob2rx('LT5*.tif'), full.names = TRUE)
listLC8<-list.files('data/', pattern = glob2rx('LC8*.tif'), full.names = TRUE)

LT5stack<-stack(listLT5)
LC8stack<-stack(listLC8)


##Step 5. Extract cloud layer from stack
clmaskLT5<-LT5stack[[1]]
clmaskLC8<-LC8stack[[1]]


##Step 6. Remove cloud layer from stack
LT5stack6<-dropLayer(LT5stack, 1)
LC8stack6<-dropLayer(LC8stack, 1)

##Step 7. Use the cloud mask function to apply a mask to the Landsat images where all values that are not land (so all clouds) = No Value
LT5CloudFree <- overlay(x = LT5stack6, y = clmaskLT5, fun = cloud2NA)
LC8CloudFree <- overlay(x = LC8stack6, y = clmaskLC8, fun = cloud2NA)

##Step 8. Apply same names from original files to the cloud mask files whose names got removed with the overlay function in step 7
names(LT5CloudFree)=names(LT5stack6)
names(LC8CloudFree)=names(LC8stack6)


##Step 9. Find only the part of the two files that intersects
inter5and8<-intersect(LT5CloudFree,LC8CloudFree)

inter8and5<-intersect(LC8CloudFree,LT5CloudFree)


##Step 10. NDVI calculation
#NDVI for LT5
ndviLT5 <- overlay(x=inter5and8[["LT51980241990098KIS00_sr_band4"]], y=inter5and8[["LT51980241990098KIS00_sr_band3"]], fun=ndvOver)

#NDVI for LC8
ndviLC8<- overlay(x=inter8and5[["LC81970242014109LGN00_sr_band5"]], y=inter8and5[["LC81970242014109LGN00_sr_band4"]], fun=ndvOver)


##Step 11. Bi-temporal difference by subtracting NDVILC8-LT5
NDVIfinal<-ndviLC8-ndviLT5

##Step 12. Plot the results
plot(NDVIfinal)



