### creates chart, using streamlit library, with the most recent csv file in working_dataset folder
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

recent_file = [f for f in os.listdir('working_dataset')][-1]

data = pd.read_csv(f'working_dataset\{recent_file}') #path folder of the data file
data = data.drop(data[data["Mileage"]<5].index)

plot = sns.regplot(x=data['Mileage'],y=data['Price'], data=data, line_kws={"color": "red"}, fit_reg=True, logx=True, truncate=True)
plt.xlabel('Mileage', fontsize = 22, labelpad=21)
plt.ylabel('Price', fontsize = 22, labelpad=21)
plt.ylim(0, 250000)
plt.xlim(0, 350000)

st.pyplot(plot.get_figure())
