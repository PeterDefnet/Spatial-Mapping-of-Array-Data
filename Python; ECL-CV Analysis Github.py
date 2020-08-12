# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 05:35:40 2020

@author: Peter
"""




import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from skimage import io, measure




filename_load = 'ECL-CV Example Data' #number on thresh, results files. 


#file_extension = 'C:/Users/babka/Desktop/'
file_extension = 'E:/Data/ProgramOutput/'
#file_extension = 'C:/Users/Peter/Desktop/Py/ECL-CV/Data/ProgramOutput/'


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
df['X'] = np.round(df.loc[:,'X'], decimals=0)
df['Y'] = np.round(df.loc[:,'Y'], decimals=0)




#Label connected regions > 0 
img_label = measure.label(img, background=0) # connectivity = Default





#Change img_label number to accurate ROI number from Imagej

img_label_mod = img_label.copy()
check = 0
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
        check += 1

        
img_label_mod = img_label_mod - 10000 #Return ROI values to normal.
img_label_mod[img_label_mod < 0] = 0 #turn all non-matching values to 0. 

print('Number of non-matching ROI centroids: ' + str(check)) # Number of non-matching ROI centroids with img_labels. 



save_folder = file_extension + str(filename_load) + '/' 




plt.figure(figsize=(12,12))
plt.rcParams.update({'font.size': 22})
plt.imshow(img_label)
plt.colorbar()
plt.title('Python-Labeled Thresholded Image')
plt.xlabel('X Pixel')
plt.ylabel('Y Pixel')
plt.tight_layout()
plt.savefig(save_folder + 'Python-Labeled Thresholded Image.png')
plt.show()    


plt.figure(figsize=(12,12))
plt.rcParams.update({'font.size': 22})
plt.imshow(img_label_mod)
plt.colorbar()
plt.title('ROI-Labeled Thresholded Image')
plt.xlabel('X Pixel')
plt.ylabel('Y Pixel')
plt.tight_layout()
plt.savefig(save_folder + 'Reassigned Python Thresholded Image.png')
plt.show()



#Now values in img_label_mod correspond to ROI #'s in res_sort
#Therefore, analyses done with res_sort can be heatmapped by changing ROI values in ndarray img_label_mod to desired statistic.  
#Next, use res_sort to do analyses on ECL-CV data. 



'''Create df's used for analysis functions'''

df = res_sort[['Mean', 'Slice', 'ROI']]
df_sort = df.sort_values(['ROI', 'Slice'], ascending = (True, True))







'''Map which ROI's turn on at thresholded Intensity + Plot Histogram of results'''


def map_threshold(df_sort, threshold):
    '''Input dataframe with columns labeled 'Mean', 'Slice', 'ROI' 
    Output df with rows as ROI, Mean, Slice where threshold value occurs in each ROI'''

        
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
        thresholded_frame = pd.DataFrame(current_roi.iloc[np.argmax(mean_col > threshold)]).T #info with thresholded frame. 
        
        save = pd.concat([save, thresholded_frame], axis = 0) #Output with thresholded info. #Slice info, ROI, intensity
    
    save.reset_index(inplace=True, drop=True)   



    map_threshold_slice = img_label_mod.copy()
    for i in range(1, int(np.max(save.ROI))+1): #Changes value of img_label_mod to slice # of threshold. 
        current_row = save.loc[save['ROI'] == i]
        
        roi_num = int(current_row['ROI'][i-1]) #int #since index increments, and is 1 behind iterator. 
        slice_num = int(current_row['Slice'][i-1]) #int
            
        #map slice
        map_threshold_slice = np.where(map_threshold_slice == roi_num, slice_num + 10000, map_threshold_slice) #Where True, yield x, otherwise yield y. 
        
    map_threshold_slice = map_threshold_slice - 10000 #Introduced offset to avoid changing    
    
    
    #Remove 0's, 1's from 'save'
    save['Slice'] = save['Slice'].replace([0 ,1], np.mean(save.Slice))
    
    
    map_threshold_mV = map_threshold_slice * (6.31)
    save['mv'] = save.Slice.apply(lambda x: x*(6.31))
    
    

    #Map Threshold mV 


    plt.figure(figsize=(12,12))
    plt.rcParams['figure.dpi'] = 300 #needed to prevent pixelation of electrodes 
    plt.rcParams.update({'font.size': 22})
    plt.imshow(map_threshold_mV, cmap= 'jet_r', vmin = save.mv.min()) #Scales so that colorbar min = first threshold.
    plt.colorbar()
    plt.title('mV with Intensity >' + str(threshold) + ' Scaled to show variation\n')
    plt.xlabel('X Pixel')
    plt.ylabel('Y Pixel')
    plt.tight_layout()
    plt.savefig(save_folder + 'Potential (mV) with Intensity larger' + str(threshold) + ' Scaled to show variation'+ '.png')
    plt.show()

    

    plt.figure(figsize=(10,10))
    plt.rcParams['figure.dpi'] = 300 #needed to prevent pixelation of electrodes     
    plt.rcParams.update({'font.size': 22})
    sns.distplot(save.mv, color = 'k', kde=False, bins = abs(int(save.mv.max() - save.mv.min()))) #1 bin per frame
    plt.xlabel('Potential (mV)')
    plt.ylabel('# of Electrodes')
    plt.title('Potential (mV) where Intensity > ' + str(threshold))
    plt.tight_layout()
    plt.savefig(save_folder + 'Potential (mV) where Intensity larger ' + str(threshold) + '_Histogram' + '.png')
    plt.show()







map_threshold(df_sort, 1000) #intensity





