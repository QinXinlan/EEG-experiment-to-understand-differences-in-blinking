# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 13:13:36 2018

@author: Eva
"""

import random

expName = ['RM','MI','RMV','MIV','SSVEP','P3004L','P3005L']

randVec = random.sample(range(1,len(expName)+1),len(expName))

for i in range(0,len(expName)):
    print('Exp '+str(i+1)+' = '+expName[randVec[i]-1])
