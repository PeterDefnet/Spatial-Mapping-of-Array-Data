
Filename_load = "ECL-CV Example Data"

file_extension = "E:/Data/ProgramOutput/" + Filename_load + "/" // extenstion for mkdir


File.makeDirectory(file_extension)
Save_threshold = file_extension + "thresh_" + Filename_load + ".tif"
Save_results = file_extension + "Results_" + Filename_load + ".txt"



//Define Thresholded image by averaging first 100 blank frames. Method used with collision data.

selectWindow(Filename_load + ".tif");

run("Duplicate...", "duplicate range=1-200");
run("Z Project...", "projection=[Average Intensity]");
run("Invert");
run("8-bit");
run("Auto Local Threshold", "method=Median radius=5 parameter_1=0 parameter_2=0 white");

run("Options...", "iterations=1 count=1 black do=Nothing"); //white objects black background
run("Watershed"); //separate particles connected by corners
run("Fill Holes"); // fill holes in roi's
run("Watershed"); // Be sure that they are separated. 

saveAs("Tiff", Save_threshold);




//Obtain data from each ROI in thresholded image.

run("Analyze Particles...", "size=5-Infinity display clear add");
run("Set Measurements...", "mean centroid area_fraction stack display redirect=None decimal=3");
roiManager("Associate", "false");
roiManager("Centered", "false");
roiManager("UseNames", "true");
selectWindow(Filename_load + ".tif");
roiManager("multi-measure measure_all");
saveAs("Results", Save_results);
