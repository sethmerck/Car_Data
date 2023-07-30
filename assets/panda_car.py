import pandas as pd 

df = pd.read_csv('test_links.csv')
df = df.dropna()
df = df.drop_duplicates(subset=['Link'])
df = df.drop(df[df["Price"]==''].index)
df = df.drop(df[df["Price"]=='Not Priced'].index)

df["Price"] = df["Price"].replace('[\D]', '', regex=True).astype(int)
df["Mileage"] = df["Mileage"].replace('[\D]', '', regex=True).astype(int)

df.to_csv('cleaned_cars_links.csv', index=False)