# Automated-Image-Analysis-of-Bipolar-Microelectrode-Array-Data
Mapping electrode response statistics using Python &amp; Imagej


**Introduction:** 

As part of my doctoral work at the University of Washington, I was fortunate to be able to use cutting-edge devices called ‘bipolar microelectrode arrays’ to spatially map dynamic microscale electrochemical processes. 

Without getting deep into the chemistry behind these experiments, we could monitor the electrochemical activity from over 6000 electrodes simultaneously using a light-generating mechanism known as ‘electro-generated chemiluminescence’ (ECL). Since the raw data exists as videos showing the intensity response from thousands of discrete electrodes, analyzing their individual behavior quickly becomes very repetitive and time intensive. 

Instead, there was clear demand for creating automated data pipelines to extract meaningful information and facilitate rapid interpretation of results. 

Here I will share a critical process that served as the backbone for many experiment-specific use cases. That is: mapping specific values (such as summary statistics) of each respective electrode to an image displaying all electrode positions. This is easily adaptable, and often quite powerful. The scripts below were used to automate the data analysis, producing meaningful results in ~ 5 minutes. 

\
**Description of Code:**

The data files exist as ~770 MB tiff stacks containing 1500 frames of 512 x 512 pixels each. They monitor a stationary position containing ~6000 individual electrodes. 

The analysis is split into two separate scripts: the first in Imagej (written in the Imagej macro language) to extract data from the tiff stack, followed by subsequent analysis in Python. 

\
**ImageJ Macro Language:**

The first step is to produce a thresholded image of electrode positions across the array. This will serve as the template for which values are mapped to in Python, and therefore it is critical that the product looks uniform, and representative of the original array. 

We start by setting up local variables to enable automatic saving, used later in the script. Filename_load is simply the name of the tiff stack as a string, and file_extension is the path where the results will be saved. The specific path for the thresholded image (.tif) and results (.txt) are defined as well. 

```Java
Filename_load = "Array 3;_2_days_later_5"
file_extension = "F:/Data/ProgramOutput/" + Filename_load + "/" // extenstion for mkdir

File.makeDirectory(file_extension)
Save_threshold = file_extension + "thresh_" + Filename_load + ".tif"
Save_results = file_extension + "Results_" + Filename_load + ".txt"
```

The general strategy will be to average the pixel intensities across 100 non-light producing frames (typically found at the start of the video). This produces a sufficient-resolution image clearly showing the array’s structure. This image is then inverted to make the electrodes white with a dark background, converted to 8-bit, and then locally thresholded.  

```Java
selectWindow(Filename_load + ".tif");
run("Duplicate...", "duplicate range=1-100");
run("Z Project...", "projection=[Average Intensity]");
run("Invert");
run("8-bit");
run("Auto Local Threshold", "method=Median radius=5 parameter_1=0 parameter_2=0 white");
```
***Insert Figure 2***
\
Figure 2 displays this process. [Label each with text above image] where Figure 2a shows a raw data frame; Figure 2b shows the result of the averaged frames improving the resolution; Figure 2c shows the inverted frame; and Figure 2d showing the result from thresholding.  We can see that the electrode shapes in Figure 2d closely represent the real structures in Figure 2b. 

Imagej offers many thresholding options, where “Auto Local Thresholding” produces the most uniform output (as opposed to applying a global threshold with “Auth Threshold”). In the GUI: selecting “Image -> Adjust -> Auto Local Threshold” and Method = “Try All”, conveniently produces a 3x3 array of results for 9 different thresholding methods. Here we selected “Median” and “Radius = 5” as producing the best uniformity for our image data – found after quick experimentation. 

The quality of the thresholded image is then improved by ensuring each electrode is separate from its neighbors (i.e. pixels are not connecting) with the “Watershed” method, and fill any holes produced during thresholding with the “Fill Holes” method. The thresholded image is then saved, and later used in Python. 

```Java
run("Options...", "iterations=1 count=1 black do=Nothing"); //white objects black background
run("Watershed"); //separate particles connected by corners
run("Fill Holes"); // fill holes in roi's
run("Watershed"); // Be sure that they are separated. 
saveAs("Tiff", Save_threshold);
```

The ROI’s are then identified from the thresholded image, applied to our (1500 frame) tiff stack, and the intensity-time data is extracted from each respective electrode position. The data is saved for later analysis in Python. 


```Java
run("Analyze Particles...", "size=1-Infinity display clear add");
run("Set Measurements...", "mean centroid area_fraction stack display redirect=None decimal=3");
roiManager("Associate", "false");
roiManager("Centered", "false");
roiManager("UseNames", "true");
selectWindow(Filename_load + ".tif");
roiManager("multi-measure measure_all");
saveAs("Results", Save_results);
```




























