# -*- coding: utf-8 -*-
"""
Cleaning and EDA code for Proposed Capstone
Data Incubator Fellowship 2nd round - July 2016

"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import webbrowser
import numpy as np
%matplotlib inline

inspections_df = pd.read_csv('Food_Establishment_Inspections.csv')

#Initial inspection
inspections_df.head()

inspections_df.info()

inspections_df.isnull().sum()

#Dropping unneeded columns for initial analysis. Will add back in specific
#columns for later full analysis.
inspections_df_2 = inspections_df.drop('DBAName', axis = 1)
inspections_df_2 = inspections_df_2.drop('LegalOwner', axis = 1)
inspections_df_2 = inspections_df_2.drop('NameLast', axis = 1)
inspections_df_2 = inspections_df_2.drop('NameFirst', axis = 1)
inspections_df_2 = inspections_df_2.drop('Comments', axis = 1)
inspections_df_2 = inspections_df_2.drop('Address', axis = 1)
inspections_df_2 = inspections_df_2.drop('City', axis = 1)
inspections_df_2 = inspections_df_2.drop('State', axis = 1)
inspections_df_2 = inspections_df_2.drop('ISSDTTM', axis = 1)
inspections_df_2 = inspections_df_2.drop('EXPDTTM', axis = 1)
inspections_df_2 = inspections_df_2.drop('RESULTDTTM', axis = 1)
inspections_df_2 = inspections_df_2.drop('VIOLDTTM', axis = 1)
inspections_df_2 = inspections_df_2.drop('StatusDate', axis = 1)
inspections_df_2 = inspections_df_2.drop('RESULT', axis = 1)
inspections_df_2 = inspections_df_2.drop('ViolDesc', axis = 1)
inspections_df_2 = inspections_df_2.drop('BusinessName', axis = 1)
inspections_df_2.head()
inspections_df_2.info()

#Variable response types as a function of columns
inspections_df_2['LICSTATUS'].value_counts()

inspections_df_2['LICENSECAT'].value_counts()

inspections_df_2['DESCRIPT'].value_counts()

inspections_df_2['Violation'].value_counts()

#Conversion of "*" response to integers and creation of new column
lst = []
inspections_df_2['ViolLevel'] = inspections_df_2['ViolLevel'].astype(str)
for i in inspections_df_2['ViolLevel']:
    lst.append(len(i))
    
inspections_df_2['ViolLevelNum'] = lst

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('ViolLevel', axis = 1)

#Categorize "ViolStatus" column
inspections_df_2['ViolTarget'] = inspections_df_2['ViolStatus'].copy()
le = LabelEncoder()
inspections_df_2['ViolTarget'] = le.fit_transform(inspections_df_2['ViolTarget'])

#LabelEncoder - 1 = Fail, 2 = Pass, 0 = Missing
inspections_df_2 = inspections_df_2[inspections_df_2['ViolTarget'] != 0]
inspections_df_2['ViolTarget'].value_counts()

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('ViolStatus', axis = 1)

#Categorize "LICSTATUS" column
inspections_df_2['LICSTATUS_encode'] = inspections_df_2['LICSTATUS'].copy()
le = LabelEncoder()
inspections_df_2['LICSTATUS_encode'] = le.fit_transform(inspections_df_2['LICSTATUS_encode'])

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('LICSTATUS', axis = 1)

#Categorize "LICENSECAT" column
inspections_df_2['LICENSECAT_encode'] = inspections_df_2['LICENSECAT'].copy()
le = LabelEncoder()
inspections_df_2['LICENSECAT_encode'] = le.fit_transform(inspections_df_2['LICENSECAT_encode'])

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('LICENSECAT', axis = 1)

#Categorize "DESCRIPT" column
inspections_df_2['DESCRIPT_encode'] = inspections_df_2['DESCRIPT'].copy()
le = LabelEncoder()
inspections_df_2['DESCRIPT_encode'] = le.fit_transform(inspections_df_2['DESCRIPT_encode'])

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('DESCRIPT', axis = 1)

#Categorize "Violation" column
inspections_df_2['Violation_encode'] = inspections_df_2['Violation'].copy()
le = LabelEncoder()
inspections_df_2['Violation_encode'] = le.fit_transform(inspections_df_2['Violation_encode'])

#Drop unneeded column
inspections_df_2 = inspections_df_2.drop('Violation', axis = 1)

#Split up "Location" into separate columns
lat = []
lon = []

for i in inspections_df_2['Location']:
    try:
        lat.append(i.split(',')[0])
        lon.append(i.split(',')[1])
    except:
        lat.append(np.nan)
        lon.append(np.nan)
        
inspections_df_2['Lat'] = lat
inspections_df_2['Lon'] = lon

lat2 = []
lat3 = []

for i in inspections_df_2['Lat']:
    try:
        lat2.append(i.split('(')[0])
        lat3.append(i.split('(')[1])
    except:
        lat2.append(np.nan)
        lat3.append(np.nan)

inspections_df_2['Lat2'] = lat3
inspections_df_2['Lat2'].head()

lon2 = []
lon3 = []

for i in inspections_df_2['Lon']:
    try:
        lon2.append(i.split(')')[0])
        lon3.append(i.split(')')[1])
    except:
        lon2.append(np.nan)
        lon3.append(np.nan)

inspections_df_2['Lon2'] = lon2
inspections_df_2['Lon2'].head()

#Drop unneeded columns, rename columns, and change column type
inspections_df_2 = inspections_df_2.drop('Location', axis = 1)
inspections_df_2 = inspections_df_2.drop('Lat', axis = 1)
inspections_df_2 = inspections_df_2.drop('Lon', axis = 1)

inspections_df_2['Lat'] = inspections_df_2['Lat2']
inspections_df_2['Lon'] = inspections_df_2['Lon2']

inspections_df_2 = inspections_df_2.drop('Lat2', axis = 1)
inspections_df_2 = inspections_df_2.drop('Lon2', axis = 1)

inspections_df_2['Lat'] = inspections_df_2['Lat'].astype(float)
inspections_df_2['Lon'] = inspections_df_2['Lon'].astype(float)

#Check on the present dataframe
inspections_df_2.info()
inspections_df_2.head()
inspections_df_2.describe()
inspections_df_2.isnull().sum()

inspections_df_2.to_csv('inspection_df_2.csv')

#sns.pairplot(inspections_df_2, diag_kind = 'kde') #Computer is struggling to 
#plot out 400K data points per plot x45 plots
sns.heatmap(inspections_df_2.corr())

#Zip and Property_ID have too many NaNs to plot out histograms. Skipping them
#for the present portion of the analysis. 
lst2 = ['LICENSENO', 'ViolLevelNum', 'ViolTarget', 'LICSTATUS_encode',
        'LICENSECAT_encode', 'DESCRIPT_encode', 'Violation_encode']
for i in lst2:
    print i
    plt.figure(1, figsize = (6,6), dpi = 100)
    #histogram plot
    plt.subplot(121)
    plt.title("Histogram")
    plt.hist(inspections_df_2[i])
   
    #box and whiskers plot 
    plt.subplot(122)
    plt.title("Box-Whiskers")
    plt.boxplot(inspections_df_2[i])
    #plt.axis('tight')
    plt.autoscale(axis = 'y', tight = True)

    plt.tight_layout()
    plt.show()


#Heatmaps using the folium package. Code edited/modified from base
# files/examples from package documentation.
def heatmap_fail(inspections_df_2):
    inspections_df_3 = inspections_df_2[inspections_df_2['ViolTarget'] == 1]
    lat = inspections_df_3['Lat'].dropna()
    lat = lat.tolist()     
    lon = inspections_df_3['Lon'].dropna()
    lon = lon.tolist()
    coordinates_fail = zip(lat, lon)    

    #Coordinates from www.findlatitudeandlongitude.com    
    heatmap_1 = folium.Map(location = [42.360447, -71.05648], zoom_start = 10)
    gradient = {0.4: 'blue', 0.2: 'green', 0.4: 'red'} 
    heatmap_1.add_children(HeatMap(coordinates_fail, radius = 10, gradient = gradient))
       
    heatmap_1.create_map(path = 'Boston_inspection_fail_heatmap.html')
    
    webbrowser.open_new("Boston_inspection_fail_heatmap.html")

heatmap_fail(inspections_df_2)

def heatmap_pass(inspections_df_2):
    inspections_df_3 = inspections_df_2[inspections_df_2['ViolTarget'] == 2]
    lat = inspections_df_3['Lat'].dropna()
    lat = lat.tolist()    
    lon = inspections_df_3['Lon'].dropna()
    lon = lon.tolist()
    coordinates_pass = zip(lat, lon)   
    
    #Coordinates from www.findlatitudeandlongitude.com  
    heatmap_1 = folium.Map(location = [42.360447, -71.05648], zoom_start = 10)
     
    heatmap_1.add_children(HeatMap(coordinates_pass, radius = 10))
       
    heatmap_1.create_map(path = 'Boston_inspection_pass_heatmap.html')
    
    webbrowser.open_new("Boston_inspection_pass_heatmap.html")

heatmap_pass(inspections_df_2)