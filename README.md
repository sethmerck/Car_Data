# READ ME

This is a personal project to aid in my search of buying another used car. 

The Python scripts I used to collect and clean used car data are located in this repository.

Text files in "assets" folder were used as lists to iterate over after being read into Python.

CSV files in "outputs" folder were then used to create Tableau dashboard located <a href="https://public.tableau.com/app/profile/sethmerck/viz/GeorgiaUsedCarData/Dashboard1">here.</a>

## How It's Made: 

**Tech used:** BeautifulSoup and Pandas libraries in Python; Tableau

I used the BeautifulSoup library in Python to scrape used car listing data in Georgia from cars.com. Then cleaned up the data collected and saved it as a CSV file using Pandas.

"get_listing_data.py" file gets zip code, mileage, price, car make and model, and associated link for every listing on cars.com with a Georgia zip code. All listings were saved in a CSV file. Data was then cleaned using pandas to create cleaned tables to be used in Tableau for data visualizations.

## Results:

I found quite a few reasonably valued cars in my area that I'm interested in. I also found a few interested details in regards to what make of cars were most widely resold in the state (Honda, Chevrolet, Nissan, Ford, Toyota) among other details which I will explain further here within the next few days.


## Optimizations:

Currently working on using GitHub Actions to automate and update data regularly. Will produce updated csv file at regular time intervals. Link tableau dashboard to this repo to have the most updated data shown on dashboard. Eventually once enough time has passed, create visualizations showing the change in dataset over time.
