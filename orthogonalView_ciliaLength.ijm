//IF images open as series:
//run("Concatenate...", "all_open open");
//run("Split Channels");
fileDir = getDirectory();

//Get Max IP of Orthogonal View for Cilia
selectWindow("C2-Untitled")
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");run("Make Binary", "method=Default background=Default calculate black");

//Get Max IP of Orthogonal View for Nuclei
selectWindow("C1-Untitled")
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");run("Make Binary", "method=Default background=Default calculate black");

//Get Max IP of Orthogonal View for NaK
selectWindow("C3-Untitled")
run("Reslice [/]...", "output=0.200 start=Left avoid");
run("Z Project...", "projection=[Max Intensity]");run("Make Binary", "method=Default background=Default calculate black");


//Subtract NaK and Nuclei from Cilia to be left with cilia layer above cells
imageCalculator("Subtract create", "MAX_Reslice of C2-Untitled","MAX_Reslice of C1-Untitled");
selectWindow("Result of MAX_Reslice of C2-Untitled");
imageCalculator("Subtract create", "Result of MAX_Reslice of C2-Untitled","MAX_Reslice of C3-Untitled");
selectWindow("Result of Result of MAX_Reslice of C2-Untitled");
//run("Invert");
selectWindow("Result of Result of MAX_Reslice of C2-Untitled");
run("Rotate 90 Degrees Left");
run("Select All");
run("Plot Profile");
Plot.getValues(xpoints, ypoints);
for (j=0; j<xpoints.length; j++){
	setResult("Distance", j, xpoints[j]);
	setResult("Gray Value", j, ypoints[j]);
	updateResults();
}
saveAs("Results", fileDir + "/Results_cilia.csv");
selectWindow("Result of Result of MAX_Reslice of C2-Untitled");
saveAs("Tiff", fileDir + "/Composite_cilia.tif");

	
	//From results files, write a script that measures cell height
	//Gray value of 0 = empty. Gray value of 250 = cells. X axis is distance.