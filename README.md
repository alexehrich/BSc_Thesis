# Data Acquisition, Processing, and Interpretationf of a single-channel surface Electromyographic sensor with Machine Learning for the Smart Wearable Therapeutic Glove

## 0. Content Overview
* Report & Presentation: contains the thesis report in `.pdf` format and the presentation in `.pptx` format.
* Firmware: contains all the codes regarding the Data Acquisition and the Real-Time Evaluation Model in `.ino` format.
* Software: contains all the codes for the Data Processing, Classification Model, Real-Time Evaluation Model and the functions used in `.py` format.

## 1. Report & Presentation

## 2. Firmware

## 3. Software
* gest_picture: folder with pictures of the gestures.
* KNN.py: code for the K-Nearest Neighbors classification model.
* LogisticRegression.py: code for the Logistic Regression classification model.
* SVC.py: code for the Support Vector Classifier classification model.
* data.csv: `.csv` file with all the features data to be used in the classification models.
* evaluation.py: code for the real-time evaluation of the model.
* functions:py: code with all the functions used for the signal processing and features extraction.
* log_reg.pkl: `.plk` file with the classification model with a higher accuracy (`real_mode.py`) to be used in the real-time evaluation of the model. 
* processing_2.py: code for all the processing and feature extraction od the signal (from importing the data until extracting the features).
* real_model.py: code for the model with higher accuracy modifying the train-test proportions.
