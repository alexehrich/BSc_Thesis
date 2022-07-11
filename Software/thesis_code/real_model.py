import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv('data.csv')
y = df.pop('gesture').values
X = df.values

pipe = Pipeline([('scaler', StandardScaler()), ('log', LogisticRegression(random_state=0, max_iter=1000))])
pipe.fit(X, y)

import pickle 
file_pipe = open('log_reg.pkl', 'wb') 
pickle.dump(pipe, file_pipe)