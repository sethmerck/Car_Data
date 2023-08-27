### creates chart, using streamlit library, with the most recent csv file in working_dataset folder
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

with open('status.log', 'r') as logs:
    lines = logs.readlines()[-6:]
    lines = [i[:10] for i in lines]

z = st.select_slider('Date Collected',options=lines, value=[1,6])

recent_file = f"test_actions{lines.index(z) + 1}.csv"

data = pd.read_csv(f'working_dataset/{recent_file}') #path folder of the data file
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

data['Car'] = data['Car'].str.split(' ')
data = data.explode('Car')
data = data.query(f"Car in {brands}")


data_grouped = data.groupby(by="Car")["Price"].agg([np.mean, np.std, 'min', 'max', 'count'])
st.dataframe(data_grouped,use_container_width=True)
