### creates chart, using streamlit library, with the most recent csv file in working_dataset folder
import os
import pandas as pd
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats


url = "https://github.com/sethmerck/Used_Cars_in_GA"
st.header('Breakdown of Used Car Listing Data in GA\nData obtained from cars.com\n\n[GitHub Repo](%s)' % url, divider='gray')
st.write("")

f = open('log.txt', 'r')
num = int(f.read())

with open('status.log', 'r') as logs:
    lines = logs.readlines()[(-1 * num):]
    lines = [datetime.datetime.strptime(i[:10], '%Y-%m-%d').date() for i in lines]

start_t = lines[0]
end_t = lines[-1]


w, z = st.select_slider('Date Collected',options=lines, value=[start_t,end_t])
    


prev_file = f"test_actions{lines.index(w)+1}.csv"
recent_file = f"test_actions{lines.index(z) + 1}.csv"

prev_data = pd.read_csv(f'working_dataset/{prev_file}')
data = pd.read_csv(f'working_dataset/{recent_file}') #path folder of the data file

prev_data = prev_data.drop(prev_data[prev_data["Mileage"]<100].index)
data = data.drop(data[data["Mileage"]<100].index)

prev_data = prev_data.drop(prev_data[prev_data["Price"]<100].index)
data = data.drop(data[data["Price"]<100].index)

prev_data_grouped = prev_data.groupby(['Zip'], as_index=False).size()
data_grouped = data.groupby(['Zip'], as_index=False).size()

prev_data_merged = pd.merge(prev_data, prev_data_grouped, on='Zip', how='left') 
data_merged = pd.merge(data, data_grouped, on='Zip', how='left')

prev_data_merged = prev_data_merged[prev_data_merged['size'] > 200]
data_merged = data_merged[data_merged['size'] > 200]

## price box plot #
# a, b = plt.subplots(1,2, figsize=(10,5))

# prev_box = prev_data_merged.boxplot(column='Price', by="Zip", rot=15, ax=b[0])
# box = data_merged.boxplot(column='Price', by="Zip", rot=15, ax=b[1])

# count = 0
# for k in b:
#     if count == 0:
#         k.set_title(f"Data Collected: {w}")
#         counts = prev_data_merged.groupby(by="Zip")["Price"].count().tolist()
#     else:
#         k.set_title(f"Data Collected: {z}")
#         counts = data_merged.groupby(by="Zip")["Price"].count().tolist()
#     k.set_xlabel('Zip', fontsize = 14, labelpad=14)
#     k.set_ylim(0, 250000)
#     k.set_ylabel('Price', fontsize = 14, labelpad=14)
#     labels = k.get_xticklabels(which='major')
#     k.set_xticks(ticks=[i for i in range(1, len(counts)+1)], labels=[f"{str(v)[12:-2]}\n n = {counts[i]}" for i, v in enumerate(labels)], fontsize=8)
#     count+=1
# a.suptitle("Price Distribution Model of Zip Codes With Over 200 Listings\n", fontsize=16)
# labels = box.get_xticklabels(which='major')

# counts = sorted_data.groupby(by="Car")["Price"].count().tolist()
# box.set_xticks(ticks=[1,2,3,4,5], labels=[f"{str(v)[12:-2]}\n n = {counts[i]}" for i, v in enumerate(labels)])

# st.pyplot(a)

### ###
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots(1, 2)
fig.suptitle("Price vs. Mileage Regression Among All Listings")
prev_plot = sns.regplot(x=prev_data['Mileage'],y=prev_data['Price'], data=prev_data, line_kws={"color": "red"}, fit_reg=True, logx=True, truncate=True, ax=ax[0])
plot = sns.regplot(x=data['Mileage'],y=data['Price'], data=data, line_kws={"color": "red"}, fit_reg=True, logx=True, truncate=True, ax=ax[1])

count = 0
for k in ax:
    if count == 0:
        counts = prev_data["Price"].count().tolist()
        k.set_title(f"Data Collected: {w}\n\nn = {counts}")
    else:
        counts = data["Price"].count().tolist()
        k.set_title(f"Data Collected: {z}\n\nn = {counts}")
    k.set_xlabel('Mileage', fontsize = 18, labelpad=18)
    
    k.set_ylabel('Price', fontsize = 18, labelpad=18)
    
    k.set_ylim(0, 250000)
    
    k.set_xlim(0, 350000)
    count+=1
###############



st.write("")

## sorts by make data ##

f = open('brands.txt')
brands = []
for i in f.readlines():
    brands.append(i.strip())

### linear regression ###

master_brand_dict = {}
for i, v in enumerate(lines[lines.index(w):lines.index(z)+1]):
    file = f"test_actions{i+1}.csv"
    df = pd.read_csv(f'working_dataset/{file}')
    df = df.drop(df[df["Mileage"]<100].index)
    df = df.drop(df[df["Price"]<100].index)

    df['Car'] = df['Car'].str.split(' ')

    df = df.explode('Car')
    
    df = df.query(f"Car in {brands}")
    
    #df = df.groupby(by="Car", as_index=False)
    #df = df[["Mileage", "Price"]]
    # ["Mileage"].agg("Mileage"=('Mileage', np.median), "Price"=('Price', np.median))

    
    # df = df.groupby('Car').agg({'Mileage': [np.median,'count'], "Price": np.median}).reset_index()

    df = df.groupby('Car', as_index=False).agg(Mileage=('Mileage', np.median),
                       Count=('Mileage', 'count'),
                       Price=('Price', np.median))
    
    # #df = df.drop(df[df["count"]<300].index)
    #df = df.rename(columns={'median': 'Mileage'})
    # brand_dict = pd.Series(df['count'].values, index=df.Car).to_dict()
    # st.write(df)
    # df = df[['Mileage', 'count', 'Car']]
    
    df.set_index('Car',inplace=True)
    brand_dict = df.to_dict('index')
    
    
    
    for key in brand_dict:
        if key in master_brand_dict:
            master_brand_dict[key].append((v, brand_dict[key]))
        else:
            list_of_two = []
            list_of_two.append((v, brand_dict[key]))
            master_brand_dict[key] = list_of_two
    
fig = plt.figure(figsize=(8,8))
for brand in master_brand_dict:
    counts = [item[1]["Count"] for item in master_brand_dict[brand]]

    count_avg = sum(counts)/len(counts)

    if count_avg > 290:
        
        x_tick_vals = [item[0] for item in master_brand_dict[brand]]
        
        x_vals = [datetime.datetime.combine(item[0], datetime.time.min).timestamp() for item in master_brand_dict[brand]]
        
        y_vals = [item[1]["Price"] for item in master_brand_dict[brand]]
        
        m, b, r_value, p_value, std_err = scipy.stats.linregress(x_vals, y_vals)
        
     
        plt.scatter(x_vals, y_vals, label=f"{brand}", s=10)
        plt.plot(x_vals, np.poly1d(np.polyfit(x_vals, y_vals, 1))(x_vals))
        plt.legend(fontsize=8, loc='upper right')
        plt.xticks(ticks=[x_vals[0], x_vals[-1]], labels=[x_tick_vals[0], x_tick_vals[-1]])
        # x_vals[int(len(x_vals)/2) + 1] x_tick_vals[int(len(x_vals)/2) + 1], 
        plt.xlabel('Date', labelpad=15)
        plt.ylabel('Median Price', labelpad=15)
    plt.title("Change in Median Price of Most Common Makes Over Time", pad=10)
st.pyplot(fig)


fig = plt.figure(figsize=(8,8))
for brand in master_brand_dict:
    counts = [item[1]["Count"] for item in master_brand_dict[brand]]

    count_avg = sum(counts)/len(counts)

    if count_avg > 290:
        
        x_tick_vals = [item[0] for item in master_brand_dict[brand]]
        
        x_vals = [datetime.datetime.combine(item[0], datetime.time.min).timestamp() for item in master_brand_dict[brand]]
        
        y_vals = [item[1]["Mileage"] for item in master_brand_dict[brand]]
        
        m, b, r_value, p_value, std_err = scipy.stats.linregress(x_vals, y_vals)
        
     
        plt.scatter(x_vals, y_vals, label=f"{brand}", s=10)
        plt.plot(x_vals, np.poly1d(np.polyfit(x_vals, y_vals, 1))(x_vals))
        plt.legend(fontsize=8, loc='upper right')
        plt.xticks(ticks=[x_vals[0], x_vals[-1]], labels=[x_tick_vals[0], x_tick_vals[-1]])
        # x_vals[int(len(x_vals)/2) + 1] x_tick_vals[int(len(x_vals)/2) + 1], 
        plt.xlabel('Date', labelpad=15)
        plt.ylabel('Median Mileage', labelpad=15)
    plt.title("Change in Median Mileage of Most Common Makes Over Time", pad=10)
st.pyplot(fig)


prev_data['Car'] = prev_data['Car'].str.split(' ')
data['Car'] = data['Car'].str.split(' ')

prev_data = prev_data.explode('Car')
data = data.explode('Car')

prev_data = prev_data.query(f"Car in {brands}")
data = data.query(f"Car in {brands}")


a, b = plt.subplots(1,2, figsize=(10,5))

sorted_prev_data = prev_data[prev_data['Car'].str.contains("Honda|Chevrolet|Nissan|Ford|Toyota")]
sorted_data = data[data['Car'].str.contains("Honda|Chevrolet|Nissan|Ford|Toyota")]
sorted_box = sorted_prev_data.boxplot(column='Price', by="Car", rot=15, ax=b[0])
box = sorted_data.boxplot(column='Price', by="Car", rot=15, ax=b[1])

count = 0
for k in b:
    if count == 0:
        k.set_title(f"Data Collected: {w}")
        counts = sorted_prev_data.groupby(by="Car")["Price"].count().tolist()
    else:
        k.set_title(f"Data Collected: {z}")
        counts = sorted_data.groupby(by="Car")["Price"].count().tolist()
    k.set_xlabel('Car Make', fontsize = 14, labelpad=14)
    k.set_ylim(0, 250000)
    k.set_ylabel('Price', fontsize = 14, labelpad=14)
    labels = k.get_xticklabels(which='major')
    k.set_xticks(ticks=[1,2,3,4,5], labels=[f"{str(v)[12:-2]}\n n = {counts[i]}" for i, v in enumerate(labels)])
    count+=1
a.suptitle("Price Distribution Model of Five Most Common Car Makes\n", fontsize=16)


st.pyplot(a)

## mileage box plot ##
a, b = plt.subplots(1,2, figsize=(10,5))

sorted_box = sorted_prev_data.boxplot(column='Mileage', by="Car", rot=15, ax=b[0])
box = sorted_data.boxplot(column='Mileage', by="Car", rot=15, ax=b[1])

count = 0
for k in b:
    if count == 0:
        k.set_title(f"Data Collected: {w}")
        counts = sorted_prev_data.groupby(by="Car")["Mileage"].count().tolist()
    else:
        k.set_title(f"Data Collected: {z}")
        counts = sorted_data.groupby(by="Car")["Mileage"].count().tolist()
    k.set_xlabel('Car Make', fontsize = 14, labelpad=14)
    k.set_ylim(-10000, 350000)
    k.set_ylabel('Mileage', fontsize = 14, labelpad=14)
    labels = k.get_xticklabels(which='major')
    k.set_xticks(ticks=[1,2,3,4,5], labels=[f"{str(v)[12:-2]}\n n = {counts[i]}" for i, v in enumerate(labels)])
    count+=1
a.suptitle("Mileage Distribution Model of Five Most Common Car Makes\n", fontsize=16)


st.pyplot(a)
st.write("")

##stat_table## 

prev_data_grouped = prev_data.groupby(by="Car")["Price"].agg([np.median, 'count'])
data_grouped = data.groupby(by="Car")["Price"].agg([np.median, 'count'])
prev_mileage_data = prev_data.groupby(by="Car")["Mileage"].agg([np.median])
mileage_data = data.groupby(by="Car")["Mileage"].agg([np.median])

data_grouped['prev_price'] = prev_data_grouped['median']
data_grouped['prev_count'] = prev_data_grouped['count']
data_grouped[f"{w} Median Mileage"] = prev_mileage_data['median']
data_grouped[f"{z} Median Mileage"] = mileage_data['median']
data_grouped['Mileage_Difference'] = mileage_data['median'] - prev_mileage_data['median']

data_grouped['diff'] = data_grouped['count'] - prev_data_grouped['count']
data_grouped['Price_Difference']= data_grouped['median'] - prev_data_grouped['median']
data_grouped.rename(columns={"median": f"{z} Median Price", "prev_price": f"{w} Median Price", "count": f"{z} Count", "prev_count": f"{w} Count", "diff": "Count_Difference"}, inplace=True)
data_grouped=data_grouped[[f"{z} Median Price", f"{w} Median Price", 'Price_Difference', f"{z} Count", f"{w} Count", "Count_Difference", f"{z} Median Mileage", f"{w} Median Mileage", "Mileage_Difference"]]
st.write(" ")
st.title("Breakdown of Make Data")
st.dataframe(data_grouped,use_container_width=True)

st.write("")

master_brand_dict = {}
for i, v in enumerate(lines[lines.index(w):lines.index(z)+1]):
    file = f"test_actions{i+1}.csv"
    df = pd.read_csv(f'working_dataset/{file}')
    df = df.drop(df[df["Mileage"]<100].index)
    df = df.drop(df[df["Price"]<100].index)
    df = df[df["Car"].str.contains('Accord')]
#     st.write(df)
#     # df['Car'] = df['Car'].str.split(' ')

    # df = df.explode('Car')
    
    # df = df.query(f"Car in {brands}")
    
    #df = df.groupby(by="Car", as_index=False)
    # df = df[["Price"]]
    # ["Mileage"].agg("Mileage"=('Mileage', np.median), "Price"=('Price', np.median))

    
    # df = df.groupby('Car').agg({'Mileage': [np.median,'count'], "Price": np.median}).reset_index()

    # df = df.groupby('Car', as_index=False).agg(Mileage=('Mileage', np.median),
    #                    Count=('Mileage', 'count'),
    #                    Price=('Price', np.median))
    
    # # #df = df.drop(df[df["count"]<300].index)
    # #df = df.rename(columns={'median': 'Mileage'})
    # # brand_dict = pd.Series(df['count'].values, index=df.Car).to_dict()
    # # st.write(df)
    # # df = df[['Mileage', 'count', 'Car']]
    
    df.set_index('Car',inplace=True)
    brand_dict = df.to_dict()
    st.write(brand_dict["Price"])
    
    
# for key in brand_dict:
#     if key in master_brand_dict:
#         master_brand_dict[key].append((v, brand_dict[key]))
#     else:
#         list_of_two = []
#         list_of_two.append((v, brand_dict[key]))
#         master_brand_dict[key] = list_of_two
# st.write(master_brand_dict["Price"])


# fig = plt.figure(figsize=(8,8))
# for brand in master_brand_dict:
#     st.write(brand)
#     # counts = [item[1]["Count"] for item in master_brand_dict[brand]]

#     # count_avg = sum(counts)/len(counts)

#     # if count_avg > 290:
        
#     x_tick_vals = [item[0] for item in master_brand_dict[brand]]
    
#     x_vals = [datetime.datetime.combine(item[0], datetime.time.min).timestamp() for item in master_brand_dict[brand]]
    
#     y_vals = [item[1]["Price"] for item in master_brand_dict[brand]]
    
#     m, b, r_value, p_value, std_err = scipy.stats.linregress(x_vals, y_vals)
    
 
#     plt.scatter(x_vals, y_vals, label=f"{brand}", s=10)
#     plt.plot(x_vals, np.poly1d(np.polyfit(x_vals, y_vals, 1))(x_vals))
#     plt.legend(fontsize=8, loc='upper right')
#     plt.xticks(ticks=[x_vals[0], x_vals[-1]], labels=[x_tick_vals[0], x_tick_vals[-1]])
#     # x_vals[int(len(x_vals)/2) + 1] x_tick_vals[int(len(x_vals)/2) + 1], 
#     plt.xlabel('Date', labelpad=15)
#     plt.ylabel('Median Price', labelpad=15)
#     plt.title("Change in Median Price of Most Common Makes Over Time", pad=10)
# st.pyplot(fig)



# st.caption("Median price of all vehicles of my make of choice (Honda) has been pretty consistent over this period of time.")
# st.caption("""I found American made cars (Chevrolet and Ford) had more listings and their price distributions skewed higher compared to the other three most common car 
#            makes (Honda, Nissan, Toyota). However, I did not find much difference in the mileage distributions for listings of these five brands. The next few weeks will be spent 
#            discovering any new insights to be found in my datasets as more data comes in. As time progresses and my dataset grows, I'd like the ability to observe any 
#            broader trends (such as noticeable changes in price) that may be occurring within my local used car market.\n\nAs of 11/8/2023: The median mileage of listings in the top 5 makes has been decreasing recently. Price distributions have remained relatively 
#            consistent. Overall that means a better value for those purchasing a used vehicle. This suggests to me that it's possible people are trying to sell their 
#            secondary or tertiary vehicles for some quick cash. Makes sense with a recession looming.""")
