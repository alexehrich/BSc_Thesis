import pyrebase
import os.path
import matplotlib.pyplot as plt
import numpy as np
import functions as fnc
import scipy as sp
from scipy import signal
import pandas as pd
import seaborn as sns


########################################################
########################################################
        #LINKS TO FIREBASE AND REAL-TIME DB
########################################################
########################################################

#Credentials to link Firebase project with Python
firebaseConfig = {
  "apiKey": "AIzaSyAwBffvO_waRFkEFjO8tJpDE4z8erMECQ0",
  "authDomain": "aehrich-database.firebaseapp.com",
  "projectId": "aehrich-database",
  "databaseURL": "https://aehrich-database-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "aehrich-database.appspot.com",
  "messagingSenderId": "710072352888",
  "appId": "1:710072352888:web:7aace7bb41b5847dcc6d8d"
}

#Initializes interaction with realtime database
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


########################################################
########################################################
            #IMPORTS SIGNALS FROM FIREBASE
########################################################
########################################################

#Get recorded signal from Fyrebase
data1 = db.child("EMGdata").child("Gesture1").get() #--> gets all the content of the node (path)
data2 = db.child("EMGdata").child("Gesture2").get()
data3 = db.child("EMGdata").child("Gesture3").get()
data4 = db.child("EMGdata").child("Gesture4").get()
data5 = db.child("EMGdata").child("Gesture5").get()


########################################################
########################################################
        #DELETE KEY FROM JSON AND APPEND TO LIST
########################################################
########################################################

#Lists that stores the recorded data
gest1= []
gest2= []
gest3= []
gest4= []
gest5= []

#Removes key from JSON and appends in list
for val1 in data1.each():
  gest1.append(val1.val())

for val2 in data2.each():
  gest2.append(val2.val())

for val3 in data3.each():
  gest3.append(val3.val())

for val4 in data4.each():
  gest4.append(val4.val())

for val5 in data5.each():
  gest5.append(val5.val())


########################################################
########################################################
                #CORRECT GESTURES LENGHT
########################################################
########################################################

gest1 = fnc.correct_length(gest1)
gest2 = fnc.correct_length(gest2)
gest4 = fnc.correct_length(gest4)
gest5 = fnc.correct_length(gest5)


########################################################
########################################################
                        #REMOVE OFFSET
########################################################
########################################################

#Creates time variable
time = np.array([i/1000 for i in range(0,len(gest1),1)])

gest1= fnc.rmv_mean(gest1,time)
gest2= fnc.rmv_mean(gest2,time)
gest3= fnc.rmv_mean(gest3,time)
gest4= fnc.rmv_mean(gest4,time)
gest5= fnc.rmv_mean(gest5,time)


########################################################
########################################################
                        #FILTER
########################################################
########################################################

gest_filtered_1 = fnc.bp_filter(gest1, 20, 450, 1000, plot=False)
gest_filtered_2 = fnc.bp_filter(gest2, 20, 450, 1000, plot=False)
gest_filtered_3 = fnc.bp_filter(gest3, 20, 450, 1000, plot=False)
gest_filtered_4 = fnc.bp_filter(gest4, 20, 450, 1000, plot=False)
gest_filtered_5 = fnc.bp_filter(gest5, 20, 450, 1000, plot=False)


gest_filtered_1 = fnc.notch_filter(gest_filtered_1, 1000, plot=False)
gest_filtered_2 = fnc.notch_filter(gest_filtered_2, 1000, plot=False)
gest_filtered_3 = fnc.notch_filter(gest_filtered_3, 1000, plot=False)
gest_filtered_4 = fnc.notch_filter(gest_filtered_4, 1000, plot=False)
gest_filtered_5 = fnc.notch_filter(gest_filtered_5, 1000, plot=False)


########################################################
########################################################
                    #PRE-PROCESSING
########################################################
########################################################

preproc_1 = fnc.features(gest_filtered_1)
preproc_2 = fnc.features(gest_filtered_2)
preproc_3 = fnc.features(gest_filtered_3)
preproc_4 = fnc.features(gest_filtered_4)
preproc_5 = fnc.features(gest_filtered_5)


########################################################
########################################################
                    #DATAFRAME
########################################################
########################################################

df_1 = pd.DataFrame(preproc_1).T
df_1.index = np.arange(1, len(df_1)+1)
df_1['gesture'] = 1

df_2 = pd.DataFrame(preproc_2).T
df_2.index = np.arange(1, len(df_2)+1)
df_2['gesture'] = 2

df_3 = pd.DataFrame(preproc_3).T
df_3.index = np.arange(1, len(df_3)+1)
df_3['gesture'] = 3

df_4 = pd.DataFrame(preproc_4).T
df_4.index = np.arange(1, len(df_4)+1)
df_4['gesture'] = 4

df_5 = pd.DataFrame(preproc_5).T
df_5.index = np.arange(1, len(df_5)+1)
df_5['gesture'] = 5

frames = [df_1, df_2, df_3, df_4, df_5]

df_gest = pd.concat(frames)
df_gest.columns = ['MAV', 'MAX', 'MIN', 'RMS', 'VAR', 'DAMV', 'DVARV', 'IASD', 'IE', 'gesture']

# Generates a csv with the features to evaluate the model
df_gest = df_gest.reset_index(drop=True)
df_gest.to_csv('datos.csv', index=False)


########################################################
########################################################
                  #CORRELATION MATRIX
########################################################
########################################################

corrMatrix = df_gest.corr()
sns.heatmap(corrMatrix, annot=True)
plt.show()