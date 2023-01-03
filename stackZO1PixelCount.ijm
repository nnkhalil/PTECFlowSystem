i = 0;

for (j = 1; j < 6; j++) {
	
	k=d2s(j,0);
	run("Clear Results");
	fileLocation = getDirectory("");
	fileName = "image00"+k;

	//normalize to step size of 0.4
	selectWindow(fileName+".nd2");
	run("Split Channels");
	selectWindow("C2-"+fileName+".nd2");
	//run("Slice Remover", "first=1 last=100 increment=2"); //only include for trials 5 and 6
	
	//preprocess
	selectWindow("C2-"+fileName+".nd2");
	waitForUser("Select the center of the stack");
	run("Subtract Background...", "rolling=50 stack");
	run("Subtract...", "value=50 stack");
	
	//make binary, erode noise, dilate features
	run("Make Binary", "method=Default background=Default calculate");
	run("Erode", "stack");
	run("Dilate", "stack");
	saveAs("Tiff", fileLocation + "/image00"+k+"_ZO1_binaryStack.tif");
	
	//save histogram data
	selectWindow("image00"+k+"_ZO1_binaryStack.tif");
	run("Histogram", "stack");
	Plot.getValues(xpoints, ypoints);
	setResult("ZO-1 3D Pixel Count", i, ypoints[255]);
	saveAs("Results", fileLocation + "/image00"+k+"_ZO1_3DPixelCount.csv");
	
}