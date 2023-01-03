//IF images open as series:
run("Concatenate...", "all_open open");
run("Split Channels");
fileDir = getDirectory("");

//Get Max IP of Orthogonal View for each channel
selectWindow("C1-Untitled")
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");

selectWindow("C2-Untitled");
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");

selectWindow("C3-Untitled");
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");

run("Merge Channels...", "c1=[MAX_Reslice of C1-Untitled] c2=[MAX_Reslice of C2-Untitled] c3=[MAX_Reslice of C3-Untitled] create");
selectWindow("Composite");
run("Make Binary", "method=Default background=Default calculate");

selectWindow("Composite");
run("Rotate 90 Degrees Left");
//run("Invert");

//Sample Cell Height from Composite

for (i=0; i<10; i++){
	selectWindow("Composite");
	roiManager("Select", i);
	run("Plot Profile");
	Plot.getValues(xpoints, ypoints);
	for (j=0; j<xpoints.length; j++){
		setResult("Distance", j, xpoints[j]);
		setResult("Gray Value", j, ypoints[j]);
		updateResults();
	}
	saveAs("Results", fileDir + "/Results_cellHeight"+i+".csv");
	run("Clear Results");
}
selectWindow("Composite");
saveAs("Tiff", fileDir + "/Composite_cellHeight.tif");

	
//run cellheight.py, a script that measures cell height from results files
//Gray value of 0 = empty. Gray value of 250 = cells. X axis is distance.