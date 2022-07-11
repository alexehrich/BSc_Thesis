import pickle
import pyrebase
import os.path
import numpy as np
import functions as fnc
import scipy as sp
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

firebaseConfig = {
  "apiKey": "AIzaSyAwBffvO_waRFkEFjO8tJpDE4z8erMECQ0",
  "authDomain": "aehrich-database.firebaseapp.com",
  "projectId": "aehrich-database",
  "databaseURL": "https://aehrich-database-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "aehrich-database.appspot.com",
  "messagingSenderId": "710072352888",
  "appId": "1:710072352888:web:7aace7bb41b5847dcc6d8d"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

data = db.child("EMGdata").child("evaluation").get() #--> gets all the content of the node (path)
gest= []

for val in data.each():
  gest.append(val.val())

gest = fnc.correct_length(gest)
time = np.array([i/1000 for i in range(0,len(gest),1)])
gest1= fnc.rmv_mean(gest,time)

gest_filtered = fnc.bp_filter(gest, 20, 450, 1000, plot=False)
gest_filtered = fnc.notch_filter(gest_filtered, 1000, plot=False)

preproc = fnc.preprocessing_3(gest_filtered)

df = pd.DataFrame(preproc).T
df.index = np.arange(1, len(df)+1)
df.columns = ['MAV', 'MAX', 'MIN', 'RMS', 'VAR', 'DAMV', 'DVARV', 'IASD', 'IE', 'MAV 2', 'MAX 2', 'MIN 2', 'RMS 2', 'VAR 2', 'DAMV 2', 'DVARV 2', 'IASD 2', 'IE 2']
df_gest = df.reset_index(drop=True)



X = df.values

filehandler = open('log_reg.pkl', 'rb') 
pipe = pickle.load(filehandler)
y = pipe.predict(X)
y2 = pipe.predict_proba(X)

print('Gesture: ' + str(y))

if y == 1:
  img = mpimg.imread('gest_pictures/gesture_1.jpeg')
  imgplot = plt.imshow(img)
  plt.title('Gesture 1: Neutral position')
  plt.axis('off')
  plt.show()

if y == 2:
  img = mpimg.imread('gest_pictures/gesture_2.jpeg')
  imgplot = plt.imshow(img)
  plt.title('Gesture 2: Fingers extension')
  plt.axis('off')
  plt.show()

if y == 3:
  img = mpimg.imread('gest_pictures/gesture_3.jpeg')
  imgplot = plt.imshow(img)
  plt.title('Gesture 3: Fingers flexion')
  plt.axis('off')
  plt.show()

if y == 4:
  img = mpimg.imread('gest_pictures/gesture_4.jpeg')
  imgplot = plt.imshow(img)
  plt.title('Gesture 4: Wrist extension')
  plt.axis('off')
  plt.show()

if y == 5:
  img = mpimg.imread('gest_pictures/gesture_5.jpeg')
  imgplot = plt.imshow(img)
  plt.title('Gesture 5: Ulnar deviation')
  plt.axis('off')
  plt.show()

np.set_printoptions(precision=2, suppress=True)
print('The probability of having predicted each gesture is: ') 
print(y2*100)


db.child('EMGdata').child('evaluation').remove()
db.child('EMGdata').child('evaluation').set(0)