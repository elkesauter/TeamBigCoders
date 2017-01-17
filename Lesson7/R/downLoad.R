downLoad<- function(url, name,ext){
    nameString<-paste0(name,'.',ext)
    download.file(url = url, destfile = nameString, method = 'auto')
    unzip(zipfile=nameString, exdir='data')
    }
    


