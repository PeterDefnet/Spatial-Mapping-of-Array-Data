**Spatially Mapping Bipolar ECL Microelectrode Array Data using Python & ImageJ**

<br>

As part of my doctoral work at the University of Washington, I experimented with newly designed microfabricated devices called 'bipolar microelectrode arrays' to map redox reactions over a wide sensing area. Our lab had developed the wireless devices to allow >6000 electrodes to be monitored simultaneously using generated light intensity as the indicator of their activity. Our work improved the spatial resoluiton compared with similar devices in literature by over 20 times. 


**Yet, their usage posed a real challenge: _How can we represent this complex video data recorded from >6000 unique locations in a digestable format?_** The ability to interpret **where** reactions were occurring was important, and thus an image mapping approach was used. 


Therefore, I created a data pipeline that efficiently interprets light intensity data and maps summarized values to the respective locations from where they originated. The code is easily adaptable to select which values to map, depending on their experimental importance. 

<br>

In the example outlined here, we are using the array to screen electrocatalyst behavior. For the sake of simplicity I've decided to demo this code with a control example: where half the array is coated with a known electrocatalyst material, and the other half is bare with a non-electrocatalytic surface. We simply wanted to know which electrodes demonstrated the best electrocatalytic activity. This is accomplished by sweeping the potential in the cataltyic conditions and monitoring when light generation occurs from each electrode. The earlier the light turns on, the better electrocatalyst it is. 


I designed the program to analyze the intensity data from each electrode, find at what potential the intensity surpasses a given threshold (turns on), and map that value back onto the electrode's respective location. The mapped values are represented by different colors (referenced by the accompanying colorbar beside the plot). Therefore we can examine the generated map and easily determine which electrodes turned on at which potentials. 

<br>

Brief results from a control experiment are shown below. 
<Brightfield of Array>
<Blank thresholded Image>
<Mapped Thresholded Image>
  
 <br>
 <br>
 <br>
 

The data pipeline is split into two separate scripts: 

1. The first script (in ImageJ, written in the ImageJ Macro Language): <br>
 -- Identifies the locations of each electrode <br>
 -- Extracts and saves their intensity over time data <br>
 -- Saves a thresholded image of the array that is used to map values onto. <br>

2. The second script (in Python): <br>
 -- Analyzes the intensity over time data from each location <br>
 -- Maps a summary statistic onto the thresholded image in its correct respective location <br>
 -- Plots the mapped figures and histograms to interpret the results. <br>

<br>

The overall analysis time takes ~ 5 minutes to complete between both scripts. Yet, the final product generates an easily-interpretable visualization summarizing the critical results of the experiment!

<br>

The respective raw data files are included, which exist as ~750 MB tiff stacks containing 1500 frames of 512 x 512 pixles

<br> 


***Please view the included Jupyter Notebook for a detailed walkthrough of this project.**

