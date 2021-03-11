# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:53:59 2018

@author: QinXinlan
"""

import os, glob, mne
from shutil import copy2
from distutils.dir_util import copy_tree

path = 'D:\\BCI\\Experiments\\Blinks and BCI\\Data'
drivePath = 'H:\\Blinks and BCI\\Data'
sep = os.sep
subdirP = 'Phantom'
subdirN = 'Neuroscan'
Cnt = '.cnt'
Csv = '.csv'

def does_drive_exist(letter):
    import win32file
    return (win32file.GetLogicalDrives() >> (ord(letter.upper()) - 65) & 1) != 0

# Going to global Neuroscan folder
os.chdir(path+sep+subdirN)
nameFiles = glob.glob('*'+Cnt)
# Copying the data to the appropriate Neuroscan folder and removing the date from the name 
if len(nameFiles)>0:
    for i in range(0,len(nameFiles)):
        newName = nameFiles[i].split('_')
        if not os.path.exists(path+sep+newName[0]+sep+subdirN):
            os.makedirs(path+sep+newName[0]+sep+subdirN)
        if not os.path.exists(path+sep+newName[0]+sep+subdirN+sep+newName[1]):
            copy2(path+sep+subdirN+sep+nameFiles[i],path+sep+newName[0]+sep+subdirN+sep+newName[1])

    # Going to the appropiate Neuroscan folder
    filePath = path+sep+newName[0]+sep+subdirN
    os.chdir(filePath)
nameFiles = glob.glob('*'+Cnt)

# Saving all the cnt files as csv
if len(nameFiles)>0:
    for i in range(0,len(nameFiles)):
        fileName = nameFiles[i]
        if not os.path.exists(fileName.split(Cnt)[0]+Csv):
            raw = mne.io.read_raw_cnt(filePath+sep+fileName,montage='standard_1020')
            # Loading the data
            raw.load_data()
            # Converting the data to panda dataframe
            data = raw.to_data_frame()
            # Saving data as csv
            nameToSave = filePath+sep+fileName.split(Cnt)[0]+Csv 
            data.to_csv(nameToSave, sep='\t')

# Starting Tobii file saving


# Going to global Phantom folder
os.chdir(path+sep+subdirP)
nameFiles = glob.glob('*.cine')
nameFiles2 = glob.glob('*.xml')

# Copying the data to the appropriate Phantom folder  and removing the date from the name
if len(nameFiles)>0:
    for i in range(0,len(nameFiles)):
        newName = nameFiles[i].split('_')
        foldName = newName[0]
        if not os.path.exists(path+sep+newName[0]+sep+subdirP):
            os.makedirs(path+sep+newName[0]+sep+subdirP)
        if newName[1] not in os.listdir(path+sep+newName[0]+sep+subdirP):
            copy2(path+sep+subdirP+sep+nameFiles[i],path+sep+newName[0]+sep+subdirP+sep+newName[1])
    
if len(nameFiles2)>0:
    for i in range(0,len(nameFiles2)):
        newName2 = nameFiles2[i].split('_')
        if newName2[1] not in os.listdir(path+sep+newName2[0]+sep+subdirP):
            copy2(path+sep+subdirP+sep+nameFiles2[i],path+sep+newName2[0]+sep+subdirP+sep+newName2[1])

# Going to the today folder
os.chdir('..')
os.chdir('..')
if does_drive_exist('H'):
    copy_tree(path+sep+foldName, drivePath+sep+foldName)
else:
    print('WD My Book drive is not attached')
