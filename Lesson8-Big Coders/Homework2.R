## Libraries
library(raster)
library(hydroGOF)

load("data/GewataB2.rda")
load("data/GewataB3.rda")
load("data/GewataB4.rda")

load("data/GewataB1.rda")
load("data/GewataB5.rda")
load("data/GewataB7.rda")
load("data/vcfGewata.rda")
## Band 6 (thermal infra-red) will be excluded from this exercise



## Build a brick containing all data
alldata <- brick(GewataB1, GewataB2, GewataB3, GewataB4, GewataB5, GewataB7, vcfGewata)
names(alldata) <- c("band1", "band2", "band3", "band4", "band5", "band7", "VCF")



par(mfrow = c(1, 1)) # reset plotting window



##Step 1.a. Treat VCF Differently since it is already a product. Remove Outliers from VCF
brickNoVCF<-alldata[[-7]]

vcfGewata[vcfGewata > 100] <- NA


##Step 1.b. Remove Outliers by converting to Reflectance
reflectance<-brickNoVCF*0.0001




reflectanceB5<-reflectance[["band5"]]
reflectanceB7<-reflectance[["band7"]]

reflectanceB5[reflectanceB5 > 1] <- NA
reflectanceB7[reflectanceB7 > 1] <- NA




##Step 2. Convert back to original values and create a new brick
GewataB5new<-reflectanceB5*10000
GewataB7new<-reflectanceB7*10000



brickNoVCF2 <- brick(GewataB1, GewataB2, GewataB3, GewataB4, GewataB5new, GewataB7new)
brickNoVCF3 <- calc(brickNoVCF2, fun=function(x) x / 10000)

alldataNew <- addLayer(brickNoVCF3, vcfGewata)
names(alldataNew) <- c("band1", "band2", "band3", "band4", "band5", "band7", "VCF")


hist(alldataNew)




## Step 3. Extract all data to a data.frame
df <- as.data.frame(getValues(alldataNew))
names(df) <- c("band1", "band2", "band3", "band4", "band5", "band7", "VCF")



## Step 4. Compare data with Scatterplots
par(mfrow = c(3, 2))

plot1<-plot(band1 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5), col = "orange")
plot2<-plot(band2 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5), col = "dark green")
plot(band3 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5), col = "light blue")
plot(band4 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5), col = "red")
plot(band5 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5), col = "blue")
plot(band7 ~ VCF, data = df, pch = ".", xlim = c(0, 100), ylim = c(0, 0.5),col = "yellow")

print("Bands 4, 5, 7 don't have such a close relationship with VCF")

## Step 5. Construct Linear regression model
modelLM <- lm(VCF ~ band1 + band2 + band3 + band4 + band5 + band7, data = df)
summary(modelLM)
summary(modelLM)$r.squared 

print("All bands have a great impact on the model since they have 3***")


## Step 6. Predict land cover using the RF model
par(mfrow = c(1, 1))
predR <- predict(alldataNew, model=modelLM, na.rm=TRUE)

plot(predR)


## Step 7. RSME
VCFvar<-alldataNew[["VCF"]]
matrixVCF<-getValues(VCFvar)
matrixpredR<-getValues(predR)

library(hydroGOF)
rsme<-rmse(matrixpredR, matrixVCF, na.rm=TRUE)

## Step 8. Class differences


load("data/trainingPoly.rda")

trainingPoly@data$Code <- as.numeric(trainingPoly@data$Class)
vcf<-alldatawithoutoutlier[['VCF']]

classes <- rasterize(trainingPoly, vcf)
alldatamasked <- mask(alldataNew, classes)
names(classes) <- "class"

trainingbrick <- addLayer(alldatamasked, classes)


valuetable2 <- getValues(trainingbrick)
valuetable2 <- na.omit(valuetable2)
valuetable2 <- as.data.frame(valuetable2)
valuetable2$class <- factor(valuetable2$class, levels = c(1:3))

val_crop <- subset(valuetable2, class == 1)
val_forest <- subset(valuetable2, class == 2)
val_wetland <- subset(valuetable2, class == 3)

modellmcrop<-lm(VCF ~ band1 + band2 + band3 + band4 + band5 +  band7, data = val_crop)
modellmforest<-lm(VCF ~ band1 + band2 + band3 + band4 + band5 +  band7, data = val_forest)
modellmwetland<-lm(VCF ~ band1 + band2 + band3 + band4 + band5 +  band7, data = val_wetland)

predVCFcrop <- predict(alldataNew, model=modellmcrop, na.rm=TRUE)
predVCFforest <- predict(alldataNew, model=modellmforest, na.rm=TRUE)
predVCFwetland <- predict(alldataNew, model=modellmwetland, na.rm=TRUE)

predmatrixcrop<-getValues(predVCFcrop)
predmatrixforest<-getValues(predVCFforest)
predmatrixwetland<-getValues(predVCFwetland)


predmatrixcrop<-getValues(predVCFcrop)
predmatrixforest<-getValues(predVCFforest)
predmatrixwetland<-getValues(predVCFwetland)
vcfmatrix<-getValues(vcfGewata)

rmsecrop<-rmse(predmatrixcrop,vcfmatrix)
rmseforest<-rmse(predmatrixforest,vcfmatrix)
rmsecropwetland<-rmse(predmatrixwetland,vcfmatrix)



