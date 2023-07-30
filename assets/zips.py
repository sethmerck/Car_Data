import requests
from bs4 import BeautifulSoup as bs

url ="https://www.zipcode.com.ng/2022/06/list-of-georgia-zip-codes.html?page2#topcontent"

req = requests.get(url)
soup = bs(req.text)

soup = soup.find('tbody')
soup = soup.find_all('td')[1::4]

soup = [i.get_text() for i in soup]
with open('list.txt', 'w') as list_file:
    for i in soup:
        list_file.write(i+"\n")