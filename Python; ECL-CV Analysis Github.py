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
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 600 #Changes DPI of in-line figures.



"""Load and Clean Data""" 

#Load Directory. 
filename_load = 'ECL-CV Example Data' #number on thresh, results files. 
file_extension = 'D:/ECL Data/ProgramOutput/'
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
    
    
    plt.figure(figsize=(15, 15))
    plt.imshow(img_label)
    
    cbar = plt.colorbar()
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(28)
        
    plt.xticks(fontsize = 28)
    plt.yticks(fontsize = 28)
    plt.xlabel('X Pixel', fontsize = 32)
    plt.ylabel('Y Pixel', fontsize = 32)
    plt.title(title, fontsize = 32)
    plt.tight_layout()
    plt.savefig(save_folder + save)
    plt.show()    



#Plot Labeling before running "label_ROI()"
plot_ROI_image(img_label, title = "Python Auto-Labled Image", save = "/Python-Labeled Thresholded Image.png")

#Plot Results of "label_ROI()"
plot_ROI_image(img_label_mod, title = 'Re-Labeled ROI Image', save = '/Frame # where Intensity larger.png')


#Quite frankly, the results before and after modifying the ROI labels look exactly the same,
#But now we have the certainly that they are indeed the same!



'''Create df's used for analysis functions'''

df = res_sort[['Mean', 'Slice', 'ROI']]
df_sort = df.sort_values(['ROI', 'Slice'], ascending = (True, True))






'''Map which ROI's turn on at thresholded Intensity + Plot Histogram of results'''


def map_threshold(df_sort, threshold):
    """Maps the potential where the intensity surpasses the input 'threshold' value"""
        
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
    map_threshold_mV = map_threshold_slice * (6.31)
    save['mv'] = save.Slice.apply(lambda x: x * (6.31))    
    

    
    #Plot Histogram 
    with warnings.catch_warnings(): #Ignore warnings given by deprecation of sns.distplot()
        warnings.simplefilter("ignore")
    
        sns.distplot(save.Slice, kde=False, color = 'k',  bins = abs(int(save.Slice.max() - save.Slice.min()))) #1 bin per frame
        plt.xlabel('Frame #', fontsize = 12)
        plt.ylabel('# of Electrodes', fontsize = 12)
        
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)
        plt.title('Frame # where Intensity > ' + str(threshold), fontsize = 12)
        plt.xlim(300, 500)
        
        plt.tight_layout()
        plt.savefig(save_folder + '/Frame # where Intensity larger ' + str(threshold) + '_Histogram' + '.png', dpi = 600)
        plt.show()
    
    
    
        #Map Threshold mV  #Want base of colorbar to be black or white, but not red. 
    
        plt.figure(figsize=(12,12))
        plt.imshow(map_threshold_mV, cmap= 'jet_r', vmin = save.mv.min()-30) #Scales so that colorbar min = first threshold - 30 
        cbar = plt.colorbar()
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(28)
    
        plt.title('Comparison of Ni vs. C for HER \n', fontsize = 32)
        plt.xticks(fontsize = 32)
        plt.yticks(fontsize = 32)
        plt.xlabel('X Pixel', fontsize = 32)
        plt.ylabel('Y Pixel', fontsize = 32)
        plt.tight_layout()
        plt.savefig(save_folder + '/Potential (mV) with Intensity larger' + str(threshold) + ' Scaled to show variation'+ '.png', dpi = 600)
    
        plt.show()
        
        
    
        #Plot Histogram, KDE of Frame # where intensity threshold is.
        sns.kdeplot(save.mv, shade=True)
        plt.title('Potential (mV) where Intensity > ' + str(threshold), fontsize = 12)
        plt.xlabel('Potential (mV)', fontsize = 12)
        plt.ylabel('Density', fontsize = 12)
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)
        plt.xlim(1500, 3000)
        plt.ylim(0, 0.01)
        plt.tight_layout()
        plt.savefig(save_folder + '/Potential (mV) where Intensity larger ' + str(threshold) + '_kde' + '.png', dpi = 600)
        plt.show()
        
    


#Output Plots:
map_threshold(df_sort, 1000) # intensity 



