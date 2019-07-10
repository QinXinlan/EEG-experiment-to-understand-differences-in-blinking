To change the frequency of the video, you can use ImageMagick or Avidemux or change the code in R:

rm(list=ls())

library(animation)

#The function called to plot
toPlot <- function(Col1,Col2){
	i<-0:2; j <- 0:1;
	rect(0+2*i,0,1+2*i,1,col=Col1); rect(1+2*j,1,2+2*j,2,col=Col1); rect(0+2*i,2,1+2*i,3,col=Col1); rect(1+2*j,3,2+2*j,4,col=Col1); rect(0+2*i,4,1+2*i,5,col=Col1);
	rect(1+2*j,0,2+2*j,1,col=Col2); rect(0+2*i,1,1+2*i,2,col=Col2); rect(1+2*j,2,2+2*j,3,col=Col2); rect(0+2*i,3,1+2*i,4,col=Col2); rect(1+2*j,4,2+2*j,5,col=Col2);
}
 
# The total plot
myVid <- function(){ 
	# First plot
	dev.new(); par(bg="black"); plot(NA,xlim=c(0,5),ylim=c(0,5));

	for(i in 1:10){
		p1 <- proc.time()
		toPlot("black","white")
		p2 <- proc.time() - p1
		Sys.sleep(1 - p2[3]) #basically sleep for whatever is left of the second
		p3 <- proc.time()
		toPlot("white","black")
		p4 <- proc.time() - p3
		Sys.sleep(1 - p4[3])
	}
}

setwd("D:\\BCI\\Experiments\\Blinks and BCI\\E-Prime\\SSVEP")
#dir.create("images")
setwd("images")
png(file="image%02d.png", width=400, height=400)

for(i in 1:10){
	par(bg="black"); plot(NA,xlim=c(0,5),ylim=c(0,5)); toPlot("white","black");
	par(bg="black"); plot(NA,xlim=c(0,5),ylim=c(0,5)); toPlot("black","white");
	}
dev.off()

# convert the .png files to one .gif file using ImageMagick. 
# The system() function executes the command as if it was done
# in the terminal. the -delay flag sets the time between showing
# the frames, i.e. the speed of the animation.
system('"C:\\Program Files\\ImageMagick-7.0.5-Q16\\convert.exe" -delay 100 *.png example_1.gif')
# 1 image per second

# to not leave the directory with the single jpeg files
# I remove them.
file.remove(list.files(pattern=".png"))
