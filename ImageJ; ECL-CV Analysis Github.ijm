
// Instructions: 
// Load Script into ImageJ Macro Editor. (Accessed by "Plugins" -> "New" -> "Macro")
// Select Language to be IJ1 Macro
// Change name of 'filename_load' to match the video name to analyze
// Change directory to appropriate file saving destination
// Press 'Run'. Leave until finished (~2 min). The script is finished when the 'Run' button appears again (in the bottom left corner)

// How to avoid common errors: 
	// Make sure no ROI selections are made on the video when starting script



// Set Saving Parameters and Create Directories

filename_load = "ECL-CV Example Data" // This name should match the title of the open video. 
file_extension = "D:/ECL Data/ProgramOutput/" + filename_load + "/" // Names the folder to save data into. 

File.makeDirectory(file_extension) // Creates folder to save data into. 
Save_threshold = file_extension + "thresh_" + filename_load + ".tif" // Creates name of thresholded image file.
Save_results = file_extension + "Results_" + filename_load + ".txt" // Creates name of results data file. 



// Define Thresholded image by averaging the first 200 blank frames.
// (Averaging the noise in 200 blank frames uses the ambient light present during recording to reveal electrode locations)

selectWindow(filename_load + ".tif"); // Select window of video.

run("Duplicate...", "duplicate range=1-200"); // Duplicate frames 1-200
run("Z Project...", "projection=[Average Intensity]"); // Find Average Intensity of these first 200 frames. 
run("Invert"); // Invert the colors of Avg
run("8-bit"); // Convert to 8-bit image
run("Auto Local Threshold", "method=Median radius=5 parameter_1=0 parameter_2=0 white"); // Apply local threshold, such that the electrode locations and background are binarized.

run("Options...", "iterations=1 count=1 black do=Nothing"); // White objects, black background
run("Watershed"); // Separate the electrodes connected by corners
run("Fill Holes"); // Fill holes in electrodes, making for a more well-rounded shape. 
run("Watershed"); // Again, separate the electrodes connected by corners

saveAs("Tiff", Save_threshold); // Save thresholded image. The thresholded image serves as a blank canvas to map values onto in the .py program. 




// Obtain data from each ROI in thresholded image.

run("Analyze Particles...", "size=5-Infinity display clear add"); // Identify regions with a size of >5 pixels. Anything small is considered noise. 
run("Set Measurements...", "mean centroid area_fraction stack display redirect=None decimal=3"); // Set which values to extract in results file. 
roiManager("Associate", "false"); // Explicitly set parameters of ROI manager. 
roiManager("Centered", "false"); // Explicitly set parameters of ROI manager. 
roiManager("UseNames", "true"); // Explicitly set parameters of ROI manager. 
selectWindow(filename_load + ".tif"); // Select video.
roiManager("multi-measure measure_all"); // Extract selected values from each location identified in ROI manager. 
saveAs("Results", Save_results); // Save results as a .txt file. The intensity data will be processed in Python to summarize each electrode's individual response. 

