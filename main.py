import logging
import logging.handlers
import os
import csv
from bs4 import BeautifulSoup as bs
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    url = f"https://www.cars.com/shopping/results/?list_price_max=&makes[]=&maximum_distance=1&models[]=&page=1&page_size=100&stock_type=all&zip=30040"
    req = requests.get(url)
    if req.status_code == 200:
        zip_dict = []
        soup = bs(req.text)
        
        miles = soup.find_all('div', attrs={"class": "mileage"})
        prices = soup.find_all('span', attrs={"class": "primary-price"})
        
        count = 0
        miles_count = 1
        price_count = 0
        
        vehicles = soup.find_all('a', attrs={"class": "vehicle-card-link js-gallery-click-link"})
        new_used = soup.find_all('p', attrs={'class': 'stock-type'})
        
        for a in vehicles:
            soup_dict = {}
            if a['href'].endswith("?attribution_type=se_rp"):
                break
            else:
                if new_used[count].get_text().strip() == 'Used':
                    try:
                        soup_dict['Zip'] = "30040"
                        soup_dict['Car'] = a.get_text().strip()
                        soup_dict['Price'] = prices[price_count].get_text().strip()
                        soup_dict['Mileage'] = miles[miles_count].get_text().strip()
                        soup_dict['Link'] = "https://www.cars.com" + a['href']
                        # soup_dict[a.get_text().strip()] = [prices[price_count].get_text().strip(), miles[miles_count].get_text().strip()]
                        miles_count += 1
                        price_count += 1
                        count+=1
                    except IndexError:
                        print('error')
                        print("")
                else:
                    price_count += 1
                    count+=1
            if len(soup_dict) == 0:
                zip_dict.append({'Zip': "30040", 'Car': '', 'Price': '', 'Mileage': '', 'Link': ''})
            else:
                zip_dict.append(soup_dict)
        
        fields = ['Zip', 'Car', 'Price', 'Mileage', 'Link']
        with open("test_actions.csv", "w") as f:
             w = csv.DictWriter(f, fields)
             w.writeheader()
             w.writerows(zip_dict)
             logger.info(csv.reader(f))
