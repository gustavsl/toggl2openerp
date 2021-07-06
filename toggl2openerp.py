#!/usr/bin/env python3

import pandas as pd
import sys
import numpy as np
from datetime import datetime, timedelta

args = sys.argv
input_file = args[1]
output_file = args[2]

df = pd.read_csv(input_file, usecols=[
                 "Client", "Description", "Start date", "Duration", "Tags"], parse_dates=["Start date"])

df['Start date'] = pd.to_datetime(df['Start date'], format='%Y-%m-%d').dt.strftime('%d/%m/%Y')
df['Duration'] = pd.to_timedelta(df['Duration'])

df['Duration'] = (df['Duration'].dt.total_seconds())/3600

df.rename(columns={'Start date': 'Date', 'Client': 'Analytic Account',
                   'Duration': 'Quantity', 'Tags': 'Product'}, inplace=True)

pt = pd.pivot_table(df, index=['Date', 'Description', 'Analytic Account', 'Product'], values=[
                    'Quantity'], aggfunc='sum')

pt['General Account'] = '40005'


flattened = pd.DataFrame(pt.to_records())

cols = flattened.columns.tolist()

print(cols)

flattened = flattened[['Date', 'Analytic Account', 'Description', 'General Account', 'Product', 'Quantity']]

print(flattened)

flattened.to_csv(args[2], index=False)

print("Horas totais registradas: " + str(np.sum(flattened['Quantity'])))

#Verifica os possiveis dias que estão faltando
def missingdays(start, end, list_dates):
    while start.date() <= end.date():
        if start.weekday() not in (5,6):
            if start not in list_dates:
                print("Possivel dia faltando: " + str(start))
        start += timedelta(days=1)

worked_days = []
for date_time_flattened in flattened['Date']:
    dateTime_flattened = datetime.strptime(date_time_flattened, '%d/%m/%Y')
    worked_days.append(dateTime_flattened)

start_date = datetime.strptime(flattened['Date'][0], '%d/%m/%Y')
end_date = datetime.strptime(flattened['Date'][flattened.shape[0]-1], '%d/%m/%Y')
missingdays(start_date, end_date, worked_days)