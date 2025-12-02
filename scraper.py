import cloudscraper
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import get_stars, get_href

def scrap_page(url, scraper):
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find('ol').find_all('li')
    products_list = []
    for product in products:
        idx = product.find(class_='image_container').a.get('href').split('/')[0].split('_')[1]
        image = product.find('img').get('src').split('/')[-1]
        stars = get_stars([r for r in product.find(class_='star-rating').get("class") if r != 'star-rating'][0])
        title = product.find(class_='image_container').a.get('href').split('/')[0].split('_')[0].replace('-', ' ')
        price = float(product.find(class_="price_color").text[2:])
        in_stock = 0
        if [1 for r in product.find(class_="instock availability").i.get('class') if r == 'icon-ok'][0] == 1 : in_stock = 1
        data = {
            "id": idx,
            "image": image,
            "stars": stars, 
            "title": title, 
            "price": price, 
            "in_stock": in_stock,
        }
        products_list.append(data)
    return products_list

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

def get_book_type(product, scraper):
    href = get_href(product)
    url = f"https://books.toscrape.com/{href}"
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

p = {'id': '1000',
  'image': '2cdad67c44b002e7ead0cc35693c0e8b.jpg',
  'stars': 3,
  'title': 'a light in the attic',
  'price': 51.77,
  'in_stock': 1}

l = get_book_type(p, scraper)
