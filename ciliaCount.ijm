// select directory to store results
fileLocation = getDirectory(""); 

// loop through images 1-5 
for (i=1; i<6; i++) {
	k = d2s(i, 0); 
	
	// select cilia channel, default threshold, save number of pixels 
	selectWindow("image00" + k + ".nd2 - C=0"); 
	run("Find Maxima...", "prominence=3000 exclude output=[Point Selection]");
	run("Measure");
	saveAs("Results", fileLocation + "cilia_maxima_image00" + k + ".csv");
	run("Clear Results");
	saveAs("Tiff", fileLocation + "cilia_image00" + k + ".tif");
	
}

