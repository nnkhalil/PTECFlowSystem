//IF images open as series:
run("Concatenate...", "all_open open");
run("Split Channels");
fileLocation = getDirectory("");

//Get Max IP of Orthogonal View for each channel
selectWindow("C1-Untitled")
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");
run("Convert to Mask");

selectWindow("C2-Untitled");
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");
run("Convert to Mask");

selectWindow("C3-Untitled");
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");
run("Convert to Mask");
run("Invert");

//subtract C1 (nuclei) and C2 (Zo-1) from C3 (laminin) to be left with laminin below cells
imageCalculator("Subtract create", "MAX_Reslice of C3-Untitled","MAX_Reslice of C1-Untitled");
selectWindow("Result of MAX_Reslice of C3-Untitled");
imageCalculator("Subtract create", "Result of MAX_Reslice of C3-Untitled","MAX_Reslice of C2-Untitled");
selectWindow("Result of Result of MAX_Reslice of C3-Untitled");
run("Rotate 90 Degrees Left");

//get ROI data and save to file
for (i=0; i<10; i++){
	selectWindow("Result of Result of MAX_Reslice of C3-Untitled");
	roiManager("Select", i);
	run("Plot Profile");
	Plot.getValues(xpoints, ypoints);
	for (j=0; j<xpoints.length; j++){
		setResult("Distance", j, xpoints[j]);
		setResult("Gray Value", j, ypoints[j]);
		updateResults();
	}
	saveAs("Results", fileLocation + "/Results_lamininThickness"+i+".csv");
	run("Clear Results");
}
selectWindow("Result of Result of MAX_Reslice of C3-Untitled");
saveAs("Tiff", fileLocation + "/Composite_laminin.tif");
