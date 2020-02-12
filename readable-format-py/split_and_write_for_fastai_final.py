# -*- coding: utf-8 -*-
"""split-and-write-for-fastai-Final

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/0Bxi8S5NYOKRqRjRGd2ZXSzdKYWE3aXlTY2VKblhsVG1QeGY0
"""

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

!mkdir -p drive
!google-drive-ocamlfuse drive

import sys
sys.path.insert(0, 'drive/ASHOKA forms/')
sys.path.insert(0, 'drive/ASHOKA forms/mias_labeled/')
#sys.path.insert(1, 'drive')

import pandas as pd
from sklearn.cross_validation import  train_test_split
# https://opencv.org/
!apt-get -qq install -y libsm6 libxext6 && pip install -q -U opencv-python
import cv2
import numpy as np
import os
import glob

labels =  pd.read_csv('drive/ASHOKA forms/Labels.csv') 

print(labels.columns)                                                     
d = {'M' : 0, 'B' : 1, 'N' : 2}
labels['diagnosis'] = labels['diagnosis'].map(d)


ROOT_DIR = 'drive/ASHOKA forms/output1/'

# Put all images in the ROOT_DIR into the array named files

files = []
for file in glob.glob(ROOT_DIR + "*.pgm"):
    files.append(file)

# Create rows as many as we have at files array

row = len(files) * 3

width = 224
height = 224
num_class = 3
channel = 1
column = width * height * channel

index = 0

X= []
y=[]

for file in files:
    if index % 100 == 0:
      print(index)
    name = file.split('/')[-1]
    name = name.split('.')[0]
    img = cv2.imread(file)
    img = cv2.resize(img, (width, height))
    name = file.split('/')[-1]
    name = name.split('.')[0]
    
    X.append(  [img.ravel(), name]   )
  
    y.append(  labels[labels['Name']==name]['diagnosis'].values[0]   )
  
    index += 1

trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=25, stratify=y)

len(trainX)
for index, value in enumerate(trainX):
    print(f'{index}: {value}')

len(testY)
for index, value in enumerate(testY):
    print(f'{index}: {value}')

train_path = 'drive/ASHOKA forms/mias_labeled/train/'
subdirectory = ''
from pprint import pprint

for i in range(len(trainX)):
    if trainY[i] == 0:
        subdirectory = '/malign/'
    elif trainY[i] == 1:
        subdirectory = '/benign/'
    else:
        subdirectory = '/normal/'
    filename = trainX[i][1]
    vector = trainX[i][0]
    img = np.reshape(vector, (224, 224, 3))
    cv2.imwrite(train_path + subdirectory + filename + '.pgm', img)
    if i % 10 == 0:
        print(i)

valid_path = 'drive/ASHOKA forms/mias_labeled/valid/'
subdirectory = ''
for i in range(len(testX)):
    if testY[i] == 0:
        subdirectory = '/malign/'
    elif testY[i] == 1:
        subdirectory = '/benign/'
    else:
        subdirectory = '/normal/'
    filename = testX[i][1]
    vector = testX[i][0]
    img = np.reshape(vector, (224, 224, 3))
    cv2.imwrite(valid_path + subdirectory + filename + '.pgm', img)
    if i % 10 == 0:
        print(i)