// select directory to store results
fileLocation = getDirectory(""); 

// loop through images 1-5 
for (i=1; i<6; i++) {
	k = d2s(i, 0); 	
	
	// number of nuclei
	selectWindow("image00" + k + ".nd2 - C=2"); // nuclei channel
	run("Auto Threshold", "method=Huang white");
	run("Watershed");
	run("Analyze Particles...", "size=20-300 show=Outlines summarize");
	//before closing summary window, copy paste the number of nuclei counted in summary table
	//numNuclei = getNumber("How many nuclei were recorded in the summary table for image00" + k + "?", 100);
	}

selectWindow("Summary");
saveAs("text", fileLocation + "Results_nuclei");