import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from random import randint

df = pd.read_csv('data.csv')

y = df.pop('gesture').values
X = df.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = KNeighborsClassifier(n_neighbors=5)
pipe = Pipeline([('scaler', StandardScaler()), ('knn', clf)])

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)

accuracy1 = accuracy_score(y_test, y_pred)
print('Model: K-Nearest Neighbours')
print('[Train: 67%, Test: 33%]')
print('TEST ACCURACY IS: ' + str(accuracy1*100) + ' %')



y_train_pred = pipe.predict(X_train)
accuracy2 = accuracy_score(y_train, y_train_pred)
print('TRAINING ACCURACY IS:    ' + str(accuracy2*100) + ' %')


y_random = [randint(1,5) for _ in range(len(y_test))]
accuracy3 = accuracy_score(y_test, y_random)
print('RANDOMNESS EVALUATION IS:    ' + str(accuracy3*100) + '%')



print('CLASSIFICATION REPORT:')
print(classification_report(y_test, y_pred))



conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)
group_counts = ["{0:0.0f}".format(value) for value in conf_mat.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in conf_mat.flatten()/np.sum(conf_mat)]
labels = [f"{v1}\n{v2}\n" for v1, v2 in zip(group_counts,group_percentages)]
labels = np.asarray(labels).reshape(5,5)
ax = sns.heatmap(conf_mat, annot=labels, fmt='', cmap='Blues')
ax.set_title('Confusion Matrix \n\n')
ax.set_xlabel('\nPredicted Gesture')
ax.set_ylabel('Actual Gesture')
ax.xaxis.set_ticklabels(['Gesture 1','Gesture 2', 'Gesture 3', 'Gesture 4', 'Gesture 5'])
ax.yaxis.set_ticklabels(['Gesture 1','Gesture 2', 'Gesture 3', 'Gesture 4', 'Gesture 5'])
plt.show()