E-Prime software version I used:
2.0.10.252

* Hardware parameters
  * Check up the COM Port of your Arduino. 
  * Double click Experiment > Devices > Serial > COM Port
  * Change if necessary
  
* Software parameters
  * Press Alt + 5
  * Change if you want the times
  * With the Neuroscan trigger wire plugged in (both on the computer and on the amplifier) AND Neuroscan amplifier turned on, check the LPT port of Neuroscan
  * Change if necessary

* Display changes
If you want to change the white cross and/or the rectanges, you can edit this R code:

rm(list=ls())

horizontal_x <- c(200,600)
horizontal_y <- c(300,300)
vertical_x <- c(400,400)
vertical_y <- c(100,500)

# only white cross
dev.new();par(bg="black");plot(horizontal_x,horizontal_y,type="l",xlim=c(0,800),ylim=c(0,600),col="white"); lines(vertical_x,vertical_y,col="white")

# Right rectangle
rect_xleft <- 400
rect_ybottom <- 250
rect_xright <- 600
rect_ytop <- 350
dev.new();par(bg="black");plot(horizontal_x,horizontal_y,type="l",xlim=c(0,800),ylim=c(0,600),col="white"); rect(rect_xleft,rect_ybottom,rect_xright,rect_ytop,col="red"); lines(vertical_x,vertical_y,col="white"); lines(horizontal_x,horizontal_y,type="l",col="white"); 


# Left rectangle
rect_xleft <- 200
rect_ybottom <- 250
rect_xright <- 400
rect_ytop <- 350
dev.new();par(bg="black");plot(horizontal_x,horizontal_y,type="l",xlim=c(0,800),ylim=c(0,600),col="white"); rect(rect_xleft,rect_ybottom,rect_xright,rect_ytop,col="red"); lines(vertical_x,vertical_y,col="white"); lines(horizontal_x,horizontal_y,type="l",col="white"); 

