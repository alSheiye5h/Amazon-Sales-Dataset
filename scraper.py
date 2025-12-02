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
        type_ = get_book_type(product, scraper)
        data = {
            "id": idx,
            "image": image,
            "stars": stars, 
            "title": title, 
            "type": type_,
            "price": price, 
            "in_stock": in_stock,
        }
        products_list.append(data)
    return products_list

def get_book_type(product, scraper):
    href = get_href(product)
    url = f"https://books.toscrape.com/{href}"
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    type = soup.find(class_="breadcrumb").contents[5].a.text
    return type
