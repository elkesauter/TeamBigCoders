time<- function(name){
    #monthList<-c("January","February","March","April","May","June","July","August","September","October","November","December")
    if(name=="year"){
      nlMODISmonth<-nlMODIS
    }
    if(name=="January" | name=="February" | name== "March"|name=="April"|name=="May"|name=="June"|name=="July"|name=="August"|name=="September"|name=="October"|name=="November"|name=="December"){
      month<-name
      nlMODISmonth<-nlMODIS[[month]]
    }
    return(nlMODISmonth)
    return(month)
}










