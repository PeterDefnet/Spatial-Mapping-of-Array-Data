# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 18:00:20 2021

@author: Peter
"""

'''Experimental Parameters:'''


# scan_rate = 200 #mv/s 
# voltage_range = 3000 #mv 
# fps = 30 # For camera


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from skimage import io, measure
import warnings
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 600 #Changes DPI of in-line figures.
 


"""Load and Clean Data""" 



#Load Directory. 
filename_load = "T2" #number on thresh, results files. 
file_extension = "C:/Users/Peter/Desktop/Github/Spatially Mapping Electrode Response Data using Python & ImageJ/Github Pages Post/Program Output/"
save_folder = file_extension + str(filename_load)


#Load Thresholded Image
img = io.imread(file_extension + str(filename_load) + '/' + 'thresh_' + str(filename_load) + '.tif')




#Import ROI results df #Saved results in imagej from ROI manager. 
res = pd.read_csv(file_extension + str(filename_load) + '/' + 'Results_' + str(filename_load) + '.txt', sep = '\t')
res.columns = ['Count', 'Label', 'Mean', 'X', 'Y', '%Area', 'Slice']


#Create ROI Column
res['ROI'] = res['Label'].apply(lambda x: (x.split(":",2)[1]).split("-",1)[0]) #Select ROI # from Label. #Splitting on ":" makes sure this should always work.
res['ROI'] = res['ROI'].astype(int) #Convert ROI to integer


#df to extract Intensity-Frame profiles from. 
res_sort = res.sort_values(["ROI", "Slice"], ascending = (True, True)) #Sort by ROI, Slice#. 
res_sort.reset_index(drop=True, inplace=True)



#subset df to pull unique ROI #'s and xy coords
coords = res.drop_duplicates(['ROI'])

df = coords[['ROI', 'X', 'Y']] 
df.loc[:,'X'] = np.round(df.loc[:,'X'], decimals=0)
df.loc[:,'Y'] = np.round(df.loc[:,'Y'], decimals=0)





"""Systematically re-label the ROI #'s so that the ordering matches the ImageJ ROI #'s. (Rather than Assuming Python's assignment automatically matches)"""



def label_ROI(df):


    #Label connected regions > 0 
    img_label = measure.label(img, background=0) 
    
    
    #Change img_label number to accurate ROI number from Imagej
    
    img_label_mod = img_label.copy()
    check = []
    non_match_x=[]
    non_match_y=[]
    non_match_roi=[]
    for i in range(len(df)):
        
        roi = df.iloc[i,0]
        x = int(df.iloc[i,1]) - 1 # -1 to account for 0 index.  0-511.  Not 1-512.
        y = int(df.iloc[i,2]) - 1 # -1 to account for 0 index. 
        
        if img_label[y,x] > 0 : #if ROI coordinate matches with thresholded image
            
            img_val = img_label[y,x] #Find img_label # that ROI overalps with
            
            #Change img_label value (thresholded image) to ROI #
            img_label_mod[img_label_mod == img_val] = roi + 10000 # roi ; add offset to eliminate possibility that this values is mistakenly reassigned later in loop. 
            
        else:
            non_match_roi.append(roi) #non-matching ROI
            non_match_x.append(x) #non-matching ROI
            non_match_y.append(y) #non-matching ROI
    
            
    img_label_mod = img_label_mod - 10000 #Return ROI values to normal.
    img_label_mod[img_label_mod < 0] = 0 #turn all non-matching values to 0. 
    
    print('Number of non-matching ROI centroids: ' + str(check.count(0))) # Number of non-matching ROI centroids with img_labels. 
    
    return img_label, img_label_mod




#Run 'label_ROI()'
img_label, img_label_mod = label_ROI(df)




"""Plot Label #'s on thresholded image."""
 

def plot_ROI_image(img_label, title = "Python Auto-Labled Image", save = "/Python-Labeled Thresholded Image.png"):
    
    
    
    plt.figure(figsize=(12, 12))
    plt.imshow(img_label)
    
    cbar = plt.colorbar(fraction=0.046, pad=0.04)
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(28)
        
    plt.xticks([], [])
    plt.yticks([], [])
    plt.tight_layout()
    plt.show()    



#Plot Labeling before running "label_ROI()"
plot_ROI_image(img_label, title = "Python Auto-Labled Image", save = "/Python-Labeled Thresholded Image.png")

#Plot Results of "label_ROI()"
plot_ROI_image(img_label_mod, title = 'ROI Labeled Image', save = '/Frame # where Intensity larger.png')


#Quite frankly, the results before and after modifying the ROI labels look exactly the same,
#But now we have the certainly that they are indeed the same!



#Now values in img_label_mod correspond to ROI #'s in res_sort
#Therefore, analyses done with res_sort can be heatmapped by changing ROI values in ndarray img_label_mod to desired statistic.  
#Next, use res_sort to do analyses on ECL-CV data. 



'''Create df's used for analysis functions'''

df = res_sort[['Mean', 'Slice', 'ROI']]
df_sort = df.sort_values(['ROI', 'Slice'], ascending = (True, True))









'''Map which ROI's turn on at thresholded Intensity + Plot Histogram of results'''


def map_threshold(df_sort, threshold):
    
    #threshold = 350
    '''Input dataframe with columns labeled 'ROI', 'Mean', 'Slice' 
    Output df with rows as ROI, Mean, Slice where threshold value occurs in each ROI
    Note that plots are NOT auto-saved'''
        
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns 

    
    
    '''Determine thresholded frame for each ROI'''
    total_roi = df_sort.ROI.max()
    save = pd.DataFrame()
    for i in range(1, (total_roi + 1)): #6000+ ROI's
        
        current_roi = df_sort[df_sort['ROI'] == i] # identify single ROI
        mean_col = current_roi.Mean #select only intensity column.
        thresholded_frame = pd.DataFrame(current_roi.iloc[np.argmax(mean_col > threshold)]).T #np.argmax() finds the first instance where condition is true. 
        
        save = pd.concat([save, thresholded_frame], axis = 0) #Output with thresholded info. #Slice info, ROI, intensity
    
    save.reset_index(inplace=True, drop=True) # 'save' contans a df of frames where threshold is surpassed for all ROI's. 
    
    
    
    map_threshold_slice = img_label_mod.copy()
    for i in range(1, int(np.max(save.ROI))+1): #Changes value of img_label_mod to slice # of threshold. 
        current_row = save.loc[save['ROI'] == i]
        
        roi_num = int(current_row['ROI'][i-1]) #since index increments, and is 1 behind iterator. 
        slice_num = int(current_row['Slice'][i-1]) 
        
        #map slice
        map_threshold_slice = np.where(map_threshold_slice == roi_num, slice_num + 10000, map_threshold_slice) #Where True, yield x, otherwise yield y. 
        
    map_threshold_slice = map_threshold_slice - 10000 #Introduced offset to avoid re-labeling same ROI multiple times. 
    
    

    #Remove 0's, 1's from 'save'
    save['Slice'] = save['Slice'].replace([0 ,1], np.mean(save.Slice))
     
    
    
    
    #Convert Slice # to mV.
    #200 mV/s * 0.032 s/ Frame = 6.4 mV / Frame
    #3.2 mV / Frame = 100 mV per s
    map_threshold_mV = map_threshold_slice * (3.2)
    save['mv'] = save.Slice.apply(lambda x: x * (3.2)) 
    

    #Custom color map
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    

    colors1 = plt.cm.bone(np.linspace(0., 1, 1))
    colors2 = plt.cm.jet_r(np.linspace(0, 1, 255))
    
    # combine them and build a new colormap
    colors = np.vstack((colors1, colors2))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    


    range_min = 1500
    range_max = 3000
    
    #Plot Histogram 
    with warnings.catch_warnings(): #Ignore warnings given by deprecation of sns.distplot()
        warnings.simplefilter("ignore")
    
        #Map Threshold mV  #Want base of colorbar to be black or white, but not red. 
        plt.figure(figsize=(12,12))
        plt.rcParams['font.family'] = "Arial"

       
        plt.imshow(map_threshold_mV, cmap= mymap, vmin = save.mv.min()-30) #Scales so that colorbar min = first threshold - 30  #Works best for 
        cbar = plt.colorbar(fraction=0.046, pad=0.04)
        

        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(26)
            
        plt.xticks(fontsize = 28)
        plt.yticks(fontsize = 28)
        plt.xticks([], [])
        plt.yticks([], [])
        plt.tight_layout()
        plt.show()   
    

        #Plot Histogram, KDE of Potential where intensity > threshold.
        sns.kdeplot(save.mv, shade=True)
        plt.xlabel('Potential (mV)', fontsize = 12, labelpad = 10)
        plt.ylabel('Density', fontsize = 12, labelpad = 10)
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)
        plt.xlim(range_min, range_max)
        plt.ylim(0, 0.015)
        plt.tight_layout()
        plt.show()
        
    


map_threshold(df_sort, 180) # intensity 














