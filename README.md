**Spatially Mapping Bipolar Microelectrode Array Data using Python & ImageJ**

<br>

**Problem Context**

<br>

As part of my doctoral work at the University of Washington, I experimented with cutting-edge devices called 'bipolar microelectrode arrays' to map redox reactions over a wide sensing area. Our lab had developed the wireless arrays to allow >6000 electrodes to be monitored simultaneously using generated light intensity as the indicator of their activity. Our work improved the spatial resolution compared with similar devices in literature by over 20 times. 


**Yet, their usage posed a real challenge: How can we represent the video data recorded from >6000 unique locations in a digestible format?** The ability to interpret _where_ reactions were occurring was necessary, and thus an image mapping approach was used. 

<br>

**Solution Description**

<br>

To address this problem, I created a data pipeline that interprets light intensity data and maps summarized values to their respective electrode locations. The code is easily adaptable to select which values to map, depending on their experimental importance. 

In the example outlined here, we are using the array to screen electrocatalyst behavior. For the sake of simplicity, I decided to demo this code with a control example: where half the array is coated with a known electrocatalyst material, and the other half is bare with a non-electrocatalytic surface. We simply wanted to know if our method could distinguish electrocatalytic activity. This is accomplished by sweeping the potential in the catalytic conditions and monitoring when light generation occurs from each electrode. The earlier the light turns on, the better electrocatalyst it is. 


I designed the code to find the potential at which the intensity surpasses a given threshold (turns on), and map that value back onto each electrode's respective location. The mapped values are represented by different colors (referenced by the accompanying colorbar beside the plot). We can therefore examine the generated map and quickly determine if the electrocatalytic activity varies across the array.

<br>

**Example Outputs**


<br>

Below are example outputs from the program:
<Brightfield of Array>
<Blank thresholded Image>
<Labeled ROIs of Thresholded Image>
<Mapped Thresholded Image>
<histogram mV result> 
  
 <br>
 <br>
 
 **Code Description**
 
 <br>
 

The data pipeline is split into two separate scripts: 

1. The first script (in ImageJ, written in the ImageJ Macro Language): <br>
 -- Identifies the locations of each electrode <br>
 -- Extracts and saves their intensity over time data, labeled per location <br>
 -- Saves a thresholded image of the array (which serves as a blank canvas to map values onto) <br>

2. The second script (in Python): <br>
 -- Analyzes the intensity over time data from each location <br>
 -- Maps a specific value onto the thresholded image in its respective electrode location <br>
 -- Plots the mapped figures and histograms to interpret the results <br>

<br>

The overall analysis takes ~ 5 minutes to run both scripts, and the final product generates an easily-interpretable visualization summarizing the critical results of the experiment!

<br>

The raw data file is included in the repo, which exists as a ~750 MB tiff stack containing 1500 frames of 512 x 512 pixels each.

<br> 


***Please view the included Jupyter Notebook for a detailed walkthrough of this project.**

