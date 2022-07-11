from _typeshed import StrOrBytesPath
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
print("Before correction")
print(f"The length of the gestures' dataset is: {len(gest1)}")

gest1 = fnc.correct_length(gest1)
gest2 = fnc.correct_length(gest2)
gest4 = fnc.correct_length(gest4)
gest5 = fnc.correct_length(gest5)

print("After correction")
print(f"The length of the gesture 1 dataset is: {len(gest1)}")


########################################################
########################################################
                        #REMOVE OFFSET
########################################################
########################################################

#Creates time variable
time = np.array([i/1000 for i in range(0,len(gest1[:600]),1)])


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
gest_filtered_5 = fnc.notch_filter(gest_filtered_5, 1000, plot=True)


########################################################
########################################################
                    #PRE-PROCESSING
########################################################
########################################################
plt.plot(time, gest_filtered_3[:600])
plt.show()


preproc_1 = fnc.features_2(gest_filtered_1)
preproc_2 = fnc.features_2(gest_filtered_2)
preproc_3 = fnc.features_2(gest_filtered_3)
preproc_4 = fnc.features_2(gest_filtered_4)
preproc_5 = fnc.features_2(gest_filtered_5)


########################################################
########################################################
                    #DATAFRAMES
########################################################
########################################################

#dataframes with all the information
df3_1 = pd.DataFrame(preproc_1).T
df3_1.index = np.arange(1, len(df3_1)+1)
df3_1['gesture'] = 1

df3_2 = pd.DataFrame(preproc_2).T
df3_2.index = np.arange(1, len(df3_2)+1)
df3_2['gesture'] = 2

df3_3 = pd.DataFrame(preproc_3).T
df3_3.index = np.arange(1, len(df3_3)+1)
df3_3['gesture'] = 3

df3_4 = pd.DataFrame(preproc_4).T
df3_4.index = np.arange(1, len(df3_4)+1)
df3_4['gesture'] = 4

df3_5 = pd.DataFrame(preproc_5).T
df3_5.index = np.arange(1, len(df3_5)+1)
df3_5['gesture'] = 5


#concatenates df with all values
frame_all = [df3_1, df3_2, df3_3, df3_4, df3_5]
df_all = pd.concat(frame_all)
df_all.columns = ['MAV', 'MAX', 'MIN', 'RMS', 'VAR', 'DAMV', 'DVARV', 'IASD', 'IE', 'MAV 2', 'MAX 2', 'MIN 2', 'RMS 2', 'VAR 2', 'DAMV 2', 'DVARV 2', 'IASD 2', 'IE 2', 'gesture']
df_all = df_all.reset_index(drop=True)


#removes the out of range measures
df_all= df_all[df_all['MAX']<1.64].reset_index(drop = True)
df_all= df_all[df_all['MIN']>-1.64].reset_index(drop = True)


# Generates a csv with the features to evaluate the model
df_all.to_csv('data.csv', index=False)

plt.plot(time, gest_filtered_1)
plt.xlabel('Time (sec)')
plt.ylabel('EMG (mV)')
plt.title('Gesture 1')
plt.ylim(-1.7,1.7)
plt.show()

########################################################
########################################################
                  #CORRELATION MATRIX
########################################################
########################################################

#correlation matrix for df with all values
df_all = df_all.drop(columns=['gesture'])
corrMatrix_all = df_all.corr()
sns.heatmap(corrMatrix_all, annot=True)
plt.show()