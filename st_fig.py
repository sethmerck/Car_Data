import pandas as pd
import streamlit as st

data = pd.read_csv("csv_practice.csv") #path folder of the data file
st.write(data)
