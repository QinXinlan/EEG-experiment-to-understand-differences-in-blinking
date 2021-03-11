# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:45:43 2018

@author: QinXinlan
"""

#//CLIENT// Phantom

import socket, re, os, pyautogui, time
import xml.etree.ElementTree as ET
import pandas as pand

#serverNameEP = '192.168.0.116'
serverNameEP = '192.168.0.181'
serverPortEP = 5000
#server Phantom
serverNameP = '192.168.0.133'
#serverNameP = '192.168.100.107'
serverPortP = 6002

path = 'D:\\BCI\\Experiments\\Blinks and BCI\\Data'
subdirP = 'Phantom'
subdirN = 'Neuroscan'
AllInstr = ''
AllNames = ''
timeToWaitStartN = 1
timeToWaitStartP = 5
timeToWaitEndN = 1
timeToWaitEndP = 5
Xml = ".xml"
chosenFreq = 6

if os.name == 'posix':
    sep = '/'
    python = 'python3' 
elif os.name == 'nt':
    sep = '\\'
    python = 'python'
    
TaskView_x = 120
TaskView_y = 1058
    
def receiveInstruction(AllInstr,AllNames,TaskView_x,TaskView_y):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverNameEP, serverPortEP))
        s.sendall(b'Ready')
        data = s.recv(1024)
    print('Received', repr(data))
    received = data.decode('utf-8')
    nameFile = re.split('_',received)[0] # instruction in runAtStartExp.py on EPrime server: e.g. RM11 or copy
    nameDir = re.split('_',received)[1] # todaystr 
    choicePath = re.split('_',received)[2] # Start or End
    AllInstr = AllInstr + '##' + path+sep+nameDir+sep+subdirP+sep+nameFile
    AllNames = AllNames + '##' + nameFile
    if nameFile == 'exit': return(AllInstr)
    if len(received) != 0 :
        if choicePath == 'Start':
            print('Before trial begin')
            # Creating path on Neuroscan and Phantom folders
            createDir(path+sep+nameDir+sep+subdirN)
            createDir(path+sep+nameDir+sep+subdirP)
            # To avoid any wrong window problem
            pyautogui.click(TaskView_x,TaskView_y)
            # Launch and record Neuroscan at the beginning
            saveNeuroStart(path,timeToWaitStartN,nameFile,nameDir)
            # Launch and record Phantom at the beginning
            savePhantStart(path,timeToWaitStartP,nameFile)
        elif choicePath == 'End':
            print('At trial end')
            nameRealFile = re.split('##',AllNames)[len(re.split('##',AllNames))-2] # instruction from former command: e.g. RM11
            print(nameRealFile)
            time.sleep(1)
            # To avoid any wrong window problem
            pyautogui.click(TaskView_x,TaskView_y)
            # Save Phantom file   
            savePhantEnd(timeToWaitEndP,nameRealFile,nameDir)
            time.sleep(2)
            # Save Neuroscan file            
            saveNeuroEnd(timeToWaitEndN)
            # Changing the path to where Phantom file is saved
            print(path+sep+subdirP)
            os.chdir(path+sep+subdirP)
            print(path+sep+subdirP)          
            # Getting the name of the file to check: e.g. 2018-03-06_RM16.xml
            fileCheckPh = nameDir+'_'+nameRealFile+Xml 
            # waiting that the file is created
            print('Waiting for '+fileCheckPh+' to be saved')
            while(not os.path.isfile(fileCheckPh)):
                # do nothing
                pass
            time.sleep(2)
            print('We are checking :\n'+fileCheckPh)
            # Checking the number of trials in Phantom
            messageFreq,message = checkFreqNbTrial(fileCheckPh)
            print('message = '+message)
            sendInstruction(message)
    return(AllInstr,AllNames)

# Creating the directory at the beginning
def createDir(path):
    # Create the directory if it doesn't already exist
    if not os.path.isdir(path):
        os.makedirs(path)
    # Creating the sub-directory "Neuroscan"
#    if(not os.path.isdir(path+subdir)):
#        os.makedirs(path+subdir)

# Launch and Record Neuroscan
def saveNeuroStart(path,timeToWait,nameFile,nameDir):
    time.sleep(timeToWait)
    # Step 0: Change to Neuroscan Software
    logo_x = 462
    logo_y = 1060
    pyautogui.click(logo_x,logo_y)
    #pyautogui.hotkey('win', '7')  # win 7 to change to 7th position for pinned software in task bar
    print('Change to Neuroscan Software')
    time.sleep(timeToWait)
    # Step 1: Click on Play
    play_x = 55
    play_y = 56
    pyautogui.click(play_x,play_y)
    print('Clicked on Play')
    time.sleep(timeToWait+5)
    # Step 2: Click on record
    rec_x = 79
    rec_y = 59
    pyautogui.click(rec_x,rec_y)
    print('Clicked on Record')
    time.sleep(timeToWait)
#    # Step 3: Enter the path of the file
#    path_x = 1167
#    path_y = 745
#    pyautogui.click(path_x,path_y)
#    print('Clicked on path')
#    time.sleep(timeToWait)
#    pyautogui.typewrite(path,0.1)
#    go_x = 1365
#    go_y = 747
#    pyautogui.click(go_x,go_y)
#    print('Clicked on Save')
#    time.sleep(timeToWait)
    # Step 4: Enter the name of the file
#    name_x = 1178
#    name_y = 745
#    pyautogui.click(name_x,name_y)
#    time.sleep(timeToWait)
    pyautogui.typewrite(nameDir+'_'+nameFile,0.25)
    print('Entered file name'+nameDir+'_'+nameFile)
    time.sleep(timeToWait)
    # Step 5: Press Enter to Save
    pyautogui.press('enter')   
    print('Clicked on Save')


def saveNeuroEnd(timeToWait):
    time.sleep(timeToWait)
    # Step 0: Change to Neuroscan Software
    logo_x = 462
    logo_y = 1060
    pyautogui.click(logo_x,logo_y)
    #pyautogui.hotkey('win', '7')  # win 7 to change to 7th position for pinned software in task bar
    print('Changed to Neuroscan Software')
    time.sleep(timeToWait)
    # Click on stop
    stoprec_x = 132
    stoprec_y = 61
    pyautogui.click(stoprec_x,stoprec_y)
    print('Clicked on Stop')

# Launch and record Phantom at the beginning
def savePhantStart(path,timeToWait,nameFile):
    # Step 0: Change to Phantom Software
    pyautogui.hotkey('win', '6')  # win 6 to change to 6th position for pinned software in task bar
    print('Change to Phantom Software')
    time.sleep(1)
    # Step 1: Click on Live
    Live_x = 1503
    Live_y = 38
    pyautogui.click(Live_x,Live_y)
    print('Clicked on Live')
    time.sleep(1)
    # Step 1: Click on Capture
    Cap_x = 1640
    Cap_y = 1001
    pyautogui.click(Cap_x,Cap_y)
    print('Clicked on Capture')
    time.sleep(timeToWait)
    # Step 2: Press Enter = Click on "Yes" I want to remove all RAM
    pyautogui.press('left')
    pyautogui.press('enter')
    print('Clicked on Yes')
    time.sleep(timeToWait)
    # Step 3: Click on CSR Current Session Reference
    CSR_x = 1521
    CSR_y = 422
    pyautogui.click(CSR_x,CSR_y)
    print('Clicked on CSR')
    time.sleep(timeToWait)
    # Step 4: Click on Trigger
    T_x = 1746
    T_y = 997
    pyautogui.click(T_x,T_y)
    print('Clicked on Trigger')
    time.sleep(timeToWait)
	# twice to be sure
    pyautogui.click(T_x,T_y)
    time.sleep(timeToWait)
    # Step 5: Click on Yes for Delete existing RAM
    YD_x = 917
    YD_y =550
    pyautogui.click(YD_x,YD_y)
    print('Clicked on Yes Delete existing RAM')
    
# Stop and save Phantom
def savePhantEnd(timeToWait,nameFile,nameDir):
    # Step 0: Change to Phantom Software
    pyautogui.hotkey('win', '6')  # win 6 to change to 6th position for pinned software in task bar
    print('Change to Phantom Software')
    time.sleep(timeToWait)
    # Step 1: Click on Abort Recording
    AR_x = 1642
    AR_y = 1000
    pyautogui.click(AR_x,AR_y)
    print('Clicked on Abort Recording')
    time.sleep(timeToWait)
    # Step 2: Click on Yes
    AY_x = 975
    AY_y = 595
    pyautogui.click(AY_x,AY_y)
    print('Clicked on Yes')
    time.sleep(timeToWait)
    # Step 3: Click on Play
    Play_x = 1575
    Play_y = 42
    pyautogui.click(Play_x,Play_y)
    print('Clicked on Play')
    time.sleep(timeToWait)
    # Step 4: Click on Save Cine
    SC_x = 1690
    SC_y = 997
    pyautogui.click(SC_x,SC_y)
    print('Clicked on Save Cine')
    time.sleep(timeToWait)
    # Step 5: Click on File name and enter name 
    FN_x = 961
    FN_y = 605
    pyautogui.click(FN_x,FN_y)
    print('Clicked on File Name')
    time.sleep(timeToWait)
    pyautogui.typewrite(nameDir+'_'+nameFile)
    print(nameDir+'_'+nameFile)
    # Step 6: Click on XML header file
    XHF_x = 1122
    XHF_y = 713
    pyautogui.click(XHF_x,XHF_y)
    print('Clicked on XML header file')
    time.sleep(timeToWait)
    # Step 7: Click on Save
    Save_x = 1165
    Save_y = 608
    pyautogui.click(Save_x,Save_y)
    print('Clicked on Save')
    time.sleep(timeToWait)
    
# function that checks frequency of recorded xml file and total number of trials
def checkFreqNbTrial(fileCheck):
	tree = ET.parse(fileCheck)
	root = tree.getroot()
	# Checking if the first image number is 0
	if(root[0][5].text!=str(0)):
		print("Problem: the first image number is "+root[0][5].text)
	absoluteTime = pand.DataFrame(index=range(0,len(root[4])),columns=["AbsTime"], dtype='str')
	ALLMS = pand.DataFrame(index=range(0,len(root[4])),columns=["ALLMS"], dtype='int')
	sampTime = pand.DataFrame(index=range(0,len(root[4])-1),columns=["sampTime"], dtype='int')
	absoluteTime.iat[0,0] = root[3][1].text
	ALLMS.iat[0,0] = ((int(absoluteTime.iat[0,0][0:2])*60+int(absoluteTime.iat[0,0][3:5]))*60+int(absoluteTime.iat[0,0][6:8]))*1000+int(absoluteTime.iat[0,0][9:12])
	for frame in range(1,len(root[4])): # because there is Date frame and Time frame in TIMEBLOCK
		absoluteTime.iat[frame,0] = root[3][frame*2+1].text
		ALLMS.iat[frame,0] = ((int(absoluteTime.iat[frame,0][0:2])*60+int(absoluteTime.iat[frame,0][3:5]))*60+int(absoluteTime.iat[frame,0][6:8]))*1000+int(absoluteTime.iat[frame,0][9:12])
		sampTime.iat[frame-1,0] = ALLMS.iat[frame,0]-ALLMS.iat[frame-1,0]
	# checking the median frequency
	if(round(sampTime['sampTime'].median())!=chosenFreq and round(sampTime['sampTime'].median())!=(chosenFreq+1)):
		messageFreq = "Problem: sampling frequency is "+str(round(1000/sampTime['sampTime'].median()))+" Hz \n1 frame every "+str(round(sampTime['sampTime'].median()))+" ms"
	else:
		messageFreq = ""
	# checking a recording problem (no blackframes every trial)
	timeLapse = 60
	if(not any(sampTime>timeLapse)):
		message = "There is a problem of recording: check E-Prime code, it should NOT be sending data to E-Prime at the beginning of every trial"
	# checking the number of trials
	TrialsIdx = sampTime.index[sampTime.sampTime>timeLapse].tolist()
	if(len(TrialsIdx)!=round(len(TrialsIdx)/10)*10+1):
		message = "There is a problem of recording: only "+str(len(TrialsIdx))+" trials!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	#indGb = sampTime.index[sampTime.sampTime<4].tolist()[len(sampTime.index[sampTime.sampTime<4].tolist())-1]
	#indGb = TrialsIdx[round(len(TrialsIdx)/10)*10]
	indGb = TrialsIdx[len(TrialsIdx)-1]
	#if(abs(TrialsIdx[len(TrialsIdx)-1]-indGb)<10):
	#	indGb = min(TrialsIdx[len(TrialsIdx)-1],indGb)
	TrialNb = pand.DataFrame(index=range(0,len(ALLMS)),columns=["TrialNb"], dtype='str')
	TrialNb.TrialNb[indGb:len(TrialNb)]="Goodbye"
	for trNb in range(1,len(TrialsIdx)):
	#	print('trNb = '+str(trNb))
		invNb = round(len(TrialsIdx)/10)*10-(trNb-1)
	#	print('invNb = '+str(invNb))
		lenTr = len(TrialsIdx)-trNb-1
	#	print('lenTr = '+str(lenTr))
		if(trNb==1): 
				TrialNb.TrialNb[TrialsIdx[lenTr]:indGb]="Trial"+str(invNb)
	#			print("Trial"+str(invNb))
		else: 
				TrialNb.TrialNb[TrialsIdx[lenTr]:TrialsIdx[lenTr+1]]="Trial"+str(invNb)
	#			print("Trial"+str(invNb))
	if(TrialNb.iat[TrialsIdx[0],0]!='Trial1'):
		firstTr = int(re.split("Trial",TrialNb.TrialNb[TrialsIdx[0]])[1])-1
		TrialNb.TrialNb[0:TrialsIdx[0]] = "Trial"+str(firstTr)
	else:
		TrialNb.TrialNb[0:TrialsIdx[0]] = "Welcome"
	count = TrialNb.TrialNb.value_counts()
	if(not any(TrialNb.TrialNb=="Welcome")):
		message = "There is only "+str(len(count)-2)+" trials instead of 40 trials in "+fileCheck+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	else:
		message = "Everything's gonna be alright for Phantom"
	print('message = '+message)
	return(messageFreq,message)
    
def sendInstruction(message):
    #Phantom as master
    print('Sending to E-Prime')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket to local host and port
        s.bind((serverNameP,serverPortP))
        print('Bind')
        # Start listening on socket
        s.listen(10)
        print('Listen')
        # Talking to E-Prime
        print('Trying to connect')
        conn, addr = s.accept()
        print('Accepted')
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.sendall(message.encode('utf-8'))
                print('Sending')
        s.close()

# Main Code
while True:
    print('Receving instruction from E-Prime')
    AllInstr,AllNames = receiveInstruction(AllInstr,AllNames,TaskView_x,TaskView_y)
    print('AllInstr = '+AllInstr)
    print('AllNames = '+AllNames)
