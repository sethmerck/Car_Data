### creates chart, using streamlit library, with the most recent csv file in working_dataset folder
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

with open('status.log', 'r') as logs:
    lines = logs.readlines()[-6:]
    lines = [datetime.strptime(i[:10], '%Y-%m-%d').date() for i in lines]

start_t = lines[0]
end_t = lines[-1]
w, z = st.select_slider('Date Collected',options=lines, value=[start_t,end_t])

prev_file = f"test_actions{lines.index(w)+1}.csv"
recent_file = f"test_actions{lines.index(z) + 1}.csv"

prev_data = pd.read_csv(f'working_dataset/{prev_file}')
data = pd.read_csv(f'working_dataset/{recent_file}') #path folder of the data file

prev_data = prev_data.drop(prev_data[prev_data["Mileage"]<5].index)
data = data.drop(data[data["Mileage"]<5].index)

plot = sns.regplot(x=data['Mileage'],y=data['Price'], data=data, line_kws={"color": "red"}, fit_reg=True, logx=True, truncate=True)
plt.xlabel('Mileage', fontsize = 22, labelpad=21)
plt.ylabel('Price', fontsize = 22, labelpad=21)
plt.ylim(0, 250000)
plt.xlim(0, 350000)

st.write(recent_file)
st.pyplot(plot.get_figure())

f = open('brands.txt')
brands = []
for i in f.readlines():
    brands.append(i.strip())

prev_data['Car'] = prev_data['Car'].str.split(' ')
data['Car'] = data['Car'].str.split(' ')

prev_data = prev_data.explode('Car')
data = data.explode('Car')

prev_data = prev_data.query(f"Car in {brands}")
data = data.query(f"Car in {brands}")

prev_data_grouped = prev_data.groupby(by="Car")["Price"].agg([np.mean, np.std, 'min', 'max', 'count'])
data_grouped = data.groupby(by="Car")["Price"].agg([np.mean, np.std, 'min', 'max', 'count'])

data_grouped['diff'] = data_grouped['count'] - prev_data_grouped['count']
st.dataframe(data_grouped,use_container_width=True)
