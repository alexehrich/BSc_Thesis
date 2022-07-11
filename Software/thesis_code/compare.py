import pandas as pd

df = pd.read_csv('data.csv')

df = df.groupby('gesture',as_index= False)['MAV', 'MAX', 'MIN', 'RMS', 'VAR', 'DAMV', 'DVARV', 'IASD', 'IE', 'MAV 2', 'MAX 2', 'MIN 2', 'RMS 2', 'VAR 2', 'DAMV 2', 'DVARV 2', 'IASD 2', 'IE 2'].mean()
print(df)

df.to_excel('resumen.xlsx')





