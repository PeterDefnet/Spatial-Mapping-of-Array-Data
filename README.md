# Automated Image Analysis of Electrochemiluminescence Bipolar Microelectrode Array Data
\
**Spatially Mapping Electrode Response Data using Python & ImageJ**

**Introduction** 

As part of my doctoral work at the University of Washington, I was fortunate to be able to use cutting-edge devices called ‘bipolar microelectrode arrays’ to spatially map dynamic microscale electrochemical processes. 

These allowed us to monitor the electrochemical activity from > 6000 electrodes simultaneously using a light-generating mechanism known as ‘electrogenerated chemiluminescence’ (ECL). Since the raw data exists as videos showing the intensity response from thousands of discrete electrodes, analyzing their individual behavior quickly becomes very repetitive and time intensive. 

Instead, there was clear demand for creating automated data pipelines to extract meaningful information and facilitate rapid interpretation of results. 

Here I will share a critical process that served as the backbone for many experiment-specific use cases. That is: mapping specific values (such as summary statistics) of each respective electrode to an image displaying all electrode positions. This is easily adaptable, and often quite powerful. The scripts described below were used to automate the data analysis, producing meaningful results in ~ 5 minutes. 

\
The data files exist as ~750 MB tiff stacks containing 1500 frames of 512 x 512 pixels each. They monitor a stationary position containing >6000 individual electrodes. 

The analysis is split into two separate scripts: the first in Imagej (written in the Imagej macro language) to extract data from the tiff stack, followed by subsequent analysis in Python. 



\
**Please view the included Jupyter Notebook (.ipynb) for a complete walkthrough of this code.**



