fileLocation = getDirectory(""); 

for (i=1; i<6; i++) {
	k = d2s(i, 0); 
	
	// pre process Na K image
	selectWindow("image00"+k+".nd2 - C=2");
	run("Subtract Background...", "rolling=50");
	run("Gaussian Blur...", "sigma=4");
	run("Auto Threshold", "method=Huang white");
	//run("Kill Borders");
	//imageCalculator("Subtract create", "image00"+k+".nd2 - C=1","image00"+k+"-killBorders");
	
	
	// create marker image
	selectWindow("image00"+k+".nd2 - C=0");
	run("Find Maxima...", "prominence=1000 exclude output=[Point Selection]");
	newImage("marker", "8-bit black", 2560, 2160, 1);
	selectWindow("image00"+k+".nd2 - C=0");
	roiManager("Add");
	selectWindow("marker");
	roiManager("Select", (i-1)); 

	// convert markers to drawings 
	selectWindow("marker");
	run("Draw", "slice"); 
	
	// marker controlled watershed 
	run("Marker-controlled Watershed", "input=[image00"+k+".nd2 - C=2] marker=marker mask=None binary calculate use");


	// analyze particles
	run("Analyze Regions","area perimeter circularity euler_number bounding_box centroid equivalent_ellipse ellipse_elong. convexity max._feret oriented_box oriented_box_elong. geodesic tortuosity max._inscribed_disc average_thickness geodesic_elong."); //for some reason need to manually press OK on pop-up window --> is there a way to automate this?

	// save file
	saveAs("Results", fileLocation + "/image00"+k+"-watershed-Morphometry.csv");

	// save images
	selectWindow("image00"+k+".nd2 - C=2");
	saveAs("Tiff", fileLocation+"/image00"+k+".nd2 - C=2.tif");
	close();
	selectWindow("marker");
	//saveAs("Tiff",fileLocation + "/marker00"+k+".tif"); //this doesnt work, instead save the ROI manager
	close();
	selectWindow("image00"+k+"-watershed.nd2 - C=2");
	saveAs("Tiff", fileLocation+"/image00"+k+"-watershed.nd2 - C=2 Segmentation.tif");
}

//save marker ROI set (corresponds to nuclei in an image)
roiManager("Save", fileLocation+"/RoiSet_marker.zip");