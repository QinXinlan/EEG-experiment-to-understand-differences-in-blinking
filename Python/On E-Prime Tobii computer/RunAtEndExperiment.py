# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:42:52 2018

@author: QinXinlan
"""

import os, glob, re, time, subprocess
from shutil import copy2

path = 'D:\\CodeForExperiment\\E-Prime\\V10'
#path = 'D:\\BlinksandBCITobii\\2018-07-05\\EPrime'
pathCam = 'C:\\Users\\Eva\\Documents\\Tobii Studio Projects\\Test\\Usercams'
pathGaze = 'C:\\Users\\Eva\\Documents\\Tobii Studio Projects\\Test\\GazeData'
copyPath = 'D:\\BlinksandBCITobii'
sep = os.sep
subdirM = 'Motor'
subdirMV = 'MotorVib'
subdirP = 'P300'
subdirS = 'SSVEP'
subdirE = 'E-Prime'
subdirT = 'Tobii'
subdir = [subdirM,subdirMV,subdirP,subdirS]
Edat = '.edat2'
Txt = '.txt'
Xml = '.xml'
Asf = '.asf'
Tgd = '.tgd'
Em = '.eventmonitor'
ext = [Edat,Txt,Xml]

def createDir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

# obtain video durations
def getLength(filename):
  stringDur =  subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).stdout.readlines()[16]
  duration = str(stringDur).split("Duration: ")[1].split(",")[0]
  durationMin = int(duration.split(":")[1])
  return durationMin

# Going to each folder
for f in range(0,len(subdir)):
    os.chdir(path+sep+subdir[f])
    for e in range(0,len(ext)):
        nameFiles = glob.glob('*'+ext[e])
        # Only taking the appropriate Txt files
        newList = []
        if ext[e]==Txt: 
            for i in range(0,len(nameFiles)):
                if '-' in nameFiles[i]: 
                    newList.append(nameFiles[i])  
            nameFiles = newList
        # Only taking the appropriate Txt files
        newList = []
        if ext[e]==Xml: 
            for i in range(0,len(nameFiles)):
                if 'ExperimentAdvisorReport' in nameFiles[i]: 
                    newList.append(nameFiles[i])  
            nameFiles = newList
        # Copying the data to the appropriate date folder and changing the name 
        if len(nameFiles)>0:
            for i in range(0,len(nameFiles)):
                newName = re.sub('[^A-Z]', '', nameFiles[i].split('-')[0])+nameFiles[i].split('-')[1]+nameFiles[i].split('-')[2]
                # If we are copying the Xml files
                if ext[e]==Xml: 
                    newName = re.sub('[^A-Z]', '', nameFiles[i].split('-')[0])+nameFiles[i].split('-')[1]+nameFiles[i].split('-')[2]+'_'+nameFiles[i].split('-')[3]
                # if we are in P300 folder, no need to change much
                if (f==2):
                    newName = nameFiles[i].split('-')[0]+nameFiles[i].split('-')[1]+nameFiles[i].split('-')[2]
                if(f==2 and ext[e]==Xml):
                    newName = nameFiles[i].split('-')[0]+nameFiles[i].split('-')[1]+nameFiles[i].split('-')[2]+'_'+nameFiles[i].split('-')[3]
                print(newName)
                RecDate = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(nameFiles[0])))
                # if the folder doesn't exist we should create it
                createDir(copyPath+sep+RecDate+sep+subdirE)
                #print(copyPath+sep+RecDate+sep+subdirE)
                print(copyPath+sep+RecDate+sep+subdirE+sep+newName)
                print(path+sep+subdir[f]+sep+nameFiles[i])
                # and finally copy the file in it
                if newName not in os.listdir(copyPath+sep+RecDate+sep+subdirE):
                    copy2(path+sep+subdir[f]+sep+nameFiles[i],copyPath+sep+RecDate+sep+subdirE+sep+newName)

# Getting the list of files in correct time order
os.chdir(copyPath+sep+RecDate+sep+subdirE)
filesOrder = glob.glob('*'+Txt)
filesOrder.sort(key=lambda x: os.path.getmtime(x))

os.chdir(pathCam)
camFiles = glob.glob('*'+Asf)
camFiles.sort(key=lambda x: os.path.getmtime(x))
todayCam = []
for i in range(0,len(camFiles)):
    # only getting the files recorded today AND more than 5 min movies
    if RecDate == time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(camFiles[i]))) and getLength(camFiles[i])>5:
        todayCam.append(camFiles[i])
        print(camFiles[i])
        print(getLength(camFiles[i]))
if len(filesOrder)+1==len(todayCam):
    print('Getting rid of the test!!')
    todayCam = todayCam[1:len(todayCam)]
if len(filesOrder)!= len(todayCam):
    print('There is a problem!')
else:
    for i in range(0,len(todayCam)):
        newName = filesOrder[i].split(Txt)[0]+Asf
        print(newName)
        if not os.path.exists(copyPath+sep+RecDate+sep+subdirT):
            os.makedirs(copyPath+sep+RecDate+sep+subdirT)
        if newName not in os.listdir(copyPath+sep+RecDate+sep+subdirE):
            copy2(pathCam+sep+todayCam[i],copyPath+sep+RecDate+sep+subdirT+sep+newName)
