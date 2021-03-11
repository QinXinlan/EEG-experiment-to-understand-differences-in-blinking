#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:37:03 2020

@author: qinxinlan
"""
## Extract facial landmarks from subjects' pictures and calculate the five distances: 
## Left and Right Eye Width, Inner Canthi Distance, Outer Canthi Distance, and Upper Nose to Lower Chin Distance.  
## Used to create the Summary All Info Subjects.csv

# import the necessary packages
from os import listdir
from os.path import isfile
from imutils import face_utils
from collections import OrderedDict
import numpy as np
import pandas as pand
import imutils, dlib, cv2, math
import matplotlib.pyplot as plt

Jpg = '.jpg'
Csv = '.csv'
# Shape predictor
shape_predictor = "path-to-predictor/shape_predictor_68_face_landmarks.dat"
input_images = "path-to-input-images"
save_path = "path-to-save"
save_csv = "path-to-save-csv"
images = [input_images + l.split(Jpg)[0] + Jpg for l in listdir(input_images) if len(l.split(Jpg)[0])==3]

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_IDXS = OrderedDict([
 	("mouth", (48, 68)),
 	("right_eyebrow", (17, 22)),
 	("left_eyebrow", (22, 27)),
 	("right_eye", (36, 42)),
 	("left_eye", (42, 48)),
 	("nose", (27, 36)),
 	("jaw", (0, 17))
])

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
	# return the list of (x, y)-coordinates
	return coords

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
	# create two copies of the input image -- one for the
	# overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()
	# if the colors list is None, initialize it with a unique
	# color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), # mouth
            (79, 76, 240), # right_eyebrow
            (230, 159, 23), # left_eyebrow
 			(168, 100, 168), # right_eye
            (158, 163, 32), # left_eye
 			(163, 38, 32), # nose
            (180, 42, 220)] # jaw
    elif len(colors) == 3: # colors = (163, 38, 32)
        colors = list([colors]*7)    
    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_IDXS.keys()):
		# grab the (x, y)-coordinates associated with the
		# face landmark
        (j, k) = FACIAL_LANDMARKS_IDXS[name]
        pts = shape[j:k]
		# check if are supposed to draw the jawline
        if name == "jaw":
 			# since the jawline is a non-enclosed facial region,
 			# just draw lines between the (x, y)-coordinates
             for l in range(1, len(pts)):
                 ptA = tuple(pts[l - 1])
                 ptB = tuple(pts[l])
                 cv2.line(overlay, ptA, ptB, colors[i], 2)
		# otherwise, compute the convex hull of the facial
		# landmark coordinates points and display it
        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)
 	# apply the transparent overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
 	# return the output image
    return output

def pixel_distance(point1, point2):
    distPix = math.sqrt( abs(res[Sub].iloc[(point1-1)*2]-res[Sub].iloc[(point2-1)*2]) **2 
                        + abs(res[Sub].iloc[(point1-1)*2+1]-res[Sub].iloc[(point2-1)*2+1]) **2)
    return distPix

def pixel_distance_x(point1, point2):
    distPix = abs(res[Sub].iloc[(point1-1)*2]-res[Sub].iloc[(point2-1)*2])
    return distPix

def pixel_distance_y(point1, point2):
    distPix = abs(res[Sub].iloc[(point1-1)*2+1]-res[Sub].iloc[(point2-1)*2+1])
    return distPix


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)
df = pand.DataFrame(FACIAL_LANDMARKS_IDXS, columns=FACIAL_LANDMARKS_IDXS.keys())

res = list()
for p in range(1,69):
    facepart = df.iloc[0,:].index[np.logical_and((p > df.iloc[0,:]).tolist() , (p <= df.iloc[1,:]).tolist())][0]
    res.append(str(p) + '_' + facepart + '_x')
    res.append(str(p) + '_' + facepart + '_y')
res = pand.DataFrame(pand.Series(res), columns = ['FacialLandmarks'])

for image in images: # image = images[9]
    name = image.split('/')[-1].split(Jpg)[0]
    print(name)
    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(image)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    if len(rects) == 0:
        print('Problem with ' + name + '!')
    
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        # visualize all facial landmarks with a transparent overlay
        output = visualize_facial_landmarks(image, shape, colors = (163, 38, 32), alpha = 0.95)
        
        if not isfile('path-to-image/FacialLandmarks.jpg'):
            cv2.imwrite('path-to-image/FacialLandmarks.jpg', output)
    res = pand.concat([res.reset_index(drop=True), pand.Series(shape.reshape(68*2)).rename(name)], axis=1)

# The Facial Landmarks are calculated in pixels.
# Comparing two subjects cannot be done directly since the pictures might
# not be taken from the same distance.
# First need to weight them: we assume hereafter that the jaw width is 
# proportional to the skull diameter
# The skull diameter (in cm) is recorded in Participants Info.csv
Info = pand.read_csv(save_csv + 'Participants Info' + Csv)
# addRes = pand.DataFrame( ['Jaw_Width_Px', 'LE','RE','LEB','REB','IED','IEBD','OED','OEBD','NC'], columns=['FacialLandmarks'] )
addRes = pand.DataFrame( ['Jaw_Width_Px', 'LE','RE','IED','OED','NC'], columns=['FacialLandmarks'] )
for Sub in  Info['Subjects'].tolist():
    # Pixel distance jaw width between 1 and 17
    jawPix = pixel_distance(1, 17)
    SkullD = Info['Head circumference'].iloc[Info['Subjects'].tolist().index(Sub)]
    # We assume that SkullD / Jaw = 3.5 (with Jaw and SkullD in cm)
    ratioSJ = 3.5
    PixToCm = (SkullD/ratioSJ)/jawPix
    # Left Eye Width (in approx cm) between 43 and 46
    LE = pixel_distance(43, 46)*PixToCm
    # Right Eye Width (in approx cm) between 37 and 40
    RE = pixel_distance(37, 40)*PixToCm
    # # Left Eyebrow Width (in approx cm) between 23 and 27
    # LEB = pixel_distance(23, 27)*PixToCm
    # # Right Eyebrow Width (in approx cm) between 18 and 22
    # REB = pixel_distance(18, 22)*PixToCm
    # Inner eye distance (in approx cm) between 40 and 43
    IED = pixel_distance(40, 43)*PixToCm
    # Inner eyebrow distance (in approx cm) between 22 and 23
    IEBD = pixel_distance(22, 23)*PixToCm
    # Outer eye distance (in approx cm) between 37 and 46
    OED = pixel_distance(37, 46)*PixToCm
    # Outer eyebrow distance (in approx cm) between 18 and 27
    OEBD = pixel_distance(18, 27)*PixToCm
    # Distance upper nose to lower chin (in approx cm) between 28 and 9
    NC =  pixel_distance(28, 9)*PixToCm
    # Filling addRes    
    # addRes = pand.concat([addRes.reset_index(drop=True), pand.Series([jawPix,LE,RE,LEB,REB,IED,IEBD,OED,OEBD,NC]).rename(Sub)], axis=1)
    addRes = pand.concat([addRes.reset_index(drop=True), pand.Series([jawPix,LE,RE,IED,IEBD,OED,OEBD,NC]).rename(Sub)], axis=1)

# Concatenate res with addRes
res = pand.concat([res.reset_index(drop=True), addRes], axis = 0)

if not isfile(save_csv + 'Facial Landmarks' + Csv):
    res.to_csv(save_csv + 'Facial Landmarks' + Csv)

    
