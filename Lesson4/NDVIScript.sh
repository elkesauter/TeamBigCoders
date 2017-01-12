#!/bin/bash
echo "Team Big Coders: Elke and Joy"
echo "14 January 2016"
echo "Calculate LandSat NDVI"

cd ../data
inFile=input.tif
echo "The input file: $inFile"

outFile="NDIV.tif"
echo "The output file: $outFile"

#calculate NDVI
echo "calculate ndvi"
gdal_calc.py -A $inFile --A_band=4 -B $inFile --B_band=3 --outfile=$outFile --calc="(A.astype(float)-B)/(A.astype(float)+B)" --type='Float32'

#resample to a new file called NDVI2
NDVImodif2="NDVI2.tif"
echo "The modified file: $NDVImodif2"


gdalwarp -tr 60 60 $outFile $NDVImodif2 



#reproject to a new file called NDVI3
NDVImodif3="NDVI3.tif"
echo "The modified file: $NDVImodif3"


gdalwarp -t_srs EPSG:4326 $NDVImodif2 $NDVImodif3

#echo "look at some histogram statistics"
#gdalinfo -hist -stats $NDVImodif