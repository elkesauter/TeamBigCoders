#NDVI calculation
ndvOver <- function(x, y) {
    ndvi <- (x - y) / (x + y)
    return(ndvi)
}