#!/usr/bin/env python3

import pandas as pd
import sys

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
