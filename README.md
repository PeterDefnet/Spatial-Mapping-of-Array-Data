# Automated-Image-Analysis-of-Bipolar-Microelectrode-Array-Data
Mapping electrode response statistics using Python &amp; Imagej


Introduction: 

As part of my doctoral work at the University of Washington, I was fortunate to be able to use cutting-edge devices called ‘bipolar microelectrode arrays’ to spatially map dynamic microscale electrochemical processes. 

Without getting deep into the chemistry behind these experiments, we could monitor the electrochemical activity from over 6000 electrodes simultaneously using a light-generating mechanism known as ‘electro-generated chemiluminescence’ (ECL). Since the raw data exists as videos showing the intensity response from thousands of discrete electrodes, analyzing their individual behavior quickly becomes very repetitive and time intensive. 

Instead, there was clear demand for creating automated data pipelines to extract meaningful information and facilitate rapid interpretation of results. 

Here I will share a critical process that served as the backbone for many experiment-specific use cases. That is: mapping specific values (such as summary statistics) of each respective electrode to an image displaying all electrode positions. This is easily adaptable, and often quite powerful.


