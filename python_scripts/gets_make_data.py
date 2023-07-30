import pandas as pd 

f = open('brands.txt')
brands = []
for i in f.readlines():
    brands.append(i.strip())

df = pd.read_csv('cleaned_cars_links.csv')
df['Car'] = df['Car'].str.split(' ')
df = df.explode('Car')
df = df.query(f"Car in {brands}")
df.to_csv('car_make.csv', index=False)
