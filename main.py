# a project that extracts product information,
# such as names, prices, and ratings, from an online e-commerce website 
# and stores the data in a structured format like a CSV file.

# first we need to install the required libraries
# pip install selenium==4.0.0.b4    for infinite scrolling as we are scraping form AJIO
# pip install pandas
# pip install requests
# pip install beautifulsoup4 lxml
# lxml is parser for beautifulsoup4

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

s = Service("C:/Users/Khushi Nimawat/Downloads/chromedriver-win64/chromedriver-win64/chromedriver")
driver = webdriver.Chrome(service = s)
url = "https://www.ajio.com/women-handbags/c/830301004?query=%3Arelevance%3Abrand%3ACAPRESE%3Abrand%3AAisna%3Abrand%3ABerrypeckers%3Abrand%3AELLE&classifier=intent&gridColumns=3"
driver.get(url)
time.sleep(4)
height = driver.execute_script("return document.body.scrollHeight")
# print(height)
while True:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(4)
	new_height = driver.execute_script("return document.body.scrollHeight")
	if height == new_height:
		break
	height = new_height
 
# to extract data from the AJIO website
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
# print(soup)

products = soup.find_all('div', class_='item rilrtl-products-list__item item')

productNames = []
productBrand = []
productPrices = []
productRatings = []
productLink = []

for product in products:
    name = product.find('div', class_='nameCls').text if product.find('div', class_='nameCls') else 'No Name'
    brand = product.find('div', class_='brand').text if product.find('div', class_='brand') else 'No Brand'
    price = product.find('span', class_='price').text if product.find('span', class_='price') else 'No Price'
    rating = product.find('div', class_='_3GuO8').text if product.find('div', class_='_3GuO8') else 'No Rating'
    link = product.find('a', class_='rilrtl-products-list__link desktop').get('href') if product.find('a', class_='rilrtl-products-list__link desktop') else 'No Link'
    if link != 'No Link' and not link.startswith('http'):
        link = 'https://www.ajio.com' + link
    
    productNames.append(name)
    productBrand.append(brand)
    productPrices.append(price)
    productRatings.append(rating)
    productLink.append(link)

# creating a datafram to store the data 
df = pd.DataFrame({
    'Product Name': productNames,
    'Brand': productBrand,
    'Price': productPrices,
    'Rating': productRatings,
    'Link': productLink
    })
print(df)

# datafram to csv file
df.to_csv('ajio_products.csv', index=False)
