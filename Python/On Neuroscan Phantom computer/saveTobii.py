# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 14:16:20 2018

@author: QinXinlan
"""

import os, glob, pyautogui, time

waitTobii = 124
Cnt = '.cnt'
today = str(time.strftime("%Y-%m-%d"))
sep = os.sep
Neuroscan = 'Neuroscan'


parentFile = 'D:\\BCI\\Experiments\\Blinks and BCI\\Data' 
filePath = parentFile+sep+today+sep+Neuroscan

# Getting the files order
os.chdir(filePath)
names = []
filesOrder = glob.glob('*'+Cnt)
filesOrder.sort(key=lambda x:os.path.getmtime(x))
for i in range(0,len(filesOrder)): names.append(filesOrder[i].split(Cnt)[0])

print(names)

time.sleep(1)
# Step 0: Change to Teamviewer Software
pyautogui.hotkey('win','9')
time.sleep(1)
Team_x = 716
Team_y = 982
pyautogui.click(Team_x,Team_y)
print('Change to Teamviewer software')
time.sleep(1)
# Step 1: Change to Tobii Software
Other_x = 167
Other_y = 1019
pyautogui.click(Other_x,Other_y)
time.sleep(1)
T_x = 584
T_y = 1022
pyautogui.click(T_x,T_y)
print('Change to Tobii software')
time.sleep(1)
# Step 2: Click on Data Export
DE_x = 556
DE_y = 82
pyautogui.click(DE_x,DE_y)
print('Click on Data Export')
time.sleep(1)
# repeat 5 times
# position for files:
RN_x = [622,622,622,622,622]
RN_y = [682,705,728,751,773]
for nbFile in range(0,5):
    # Step 3: Click on Clear all
    CA_x = 304
    CA_y = 978
    pyautogui.click(CA_x,CA_y)
    print('Click on Clear all')
    time.sleep(1)
    # Step 4: Click on Select Data Set
    SDS_x = 110 
    SDS_y = 119
    pyautogui.click(SDS_x,SDS_y)
    print('Click on Select Data Set')
    time.sleep(1)
    # Step 5: Click on Select Full Recording
    SFR_x = 927
    SFR_y = 447
    pyautogui.click(SFR_x,SFR_y)
    print('Click on Select Full Recording')
    time.sleep(1)
    # Step 6: Click on New Test
    NT_x = 1284
    NT_y = 303
    pyautogui.click(NT_x,NT_y)
    print('Click on New Test')
    time.sleep(1)
    # Step 7: Click with right on scroll
    CRS_x = 1322
    CRS_y = 285
    pyautogui.click(CRS_x,CRS_y,button='right')
    print('Click with right on scroll')
    time.sleep(1)
    # Step 8: Click on Bottom
    B_x = 1370
    B_y = 339
    pyautogui.click(B_x,B_y)
    print('Click on Bottom')
    time.sleep(1)
    # Step 9: Click on First recording
    
    pyautogui.click(RN_x[nbFile],RN_y[nbFile])
    print('Click on '+str(nbFile+1)+' recording')
    time.sleep(1)
    # Step 10: Click on Done
    Done_x = 1296
    Done_y = 826
    pyautogui.click(Done_x,Done_y)
    print('Click on Done')
    time.sleep(1)
    # Step 11: Change File Extension to .xlsx
    FE_x = 885
    FE_y = 171
    pyautogui.click(FE_x,FE_y)
    time.sleep(1)
    FE2_x = 883
    FE2_y = 208
    pyautogui.click(FE2_x,FE2_y)
    print('Change File Extension to .xlsx')
    time.sleep(1)
    # Step 12: Click on Enter file name
    EFN_x = 1058
    EFN_y = 171
    pyautogui.click(EFN_x,EFN_y)
    print('Enter file name')
    time.sleep(1)
    # Step 13: Write First file name
    pyautogui.hotkey('Ctrl','A')
    time.sleep(1)
    pyautogui.hotkey('Ctrl','A')
    time.sleep(1)
    pyautogui.typewrite(names[len(names)-(5-nbFile)])
    print('Write '+str(nbFile+1)+' file name')
    time.sleep(1)
    # Step 14: Click on Export data
    ED_x = 198
    ED_y = 124
    pyautogui.click(ED_x,ED_y)
    print('Click on Export data')
    time.sleep(1)
    # If it is the first time it is save do the whole thing
    if nbFile==0:
        # Step 15: Go to Storage D
        D_x = 905
        D_y = 905
        pyautogui.click(D_x,D_y)
        print('Go to Storage D')
        time.sleep(1)
        # Step 16: Go to BlinksandBCITobii
        BBT_x = 940
        BBT_y = 753
        pyautogui.click(BBT_x,BBT_y)
        print('Click on BlinksandBCITobii')
        time.sleep(1)
        # Step 17: Select today folder
        # Write C to getP3005L123c to "Codecs a installer"
        pyautogui.typewrite('c')
        time.sleep(1)
        folder_x = 936
        folder_y = 904
        pyautogui.click(folder_x,folder_y)
        print('Select today folder')
        # Step 18: Click on Tobii folder
        Tobii_x = 947
        Tobii_y = 924
        pyautogui.click(Tobii_x,Tobii_y)
        print('Click on Tobii folder')
    # Step 19: Press enter
    pyautogui.hotkey('enter')
    time.sleep(waitTobii)
    pyautogui.hotkey('enter')