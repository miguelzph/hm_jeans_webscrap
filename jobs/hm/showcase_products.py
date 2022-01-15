import requests
import pandas as pd

from bs4 import BeautifulSoup
from math import ceil
from datetime import datetime


def get_a_soup(url, headers):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    return soup

def get_url_all_products(url, soup):
    '''Function to retrive a page url with all products'''
    total_products = soup.find('h2', class_='load-more-heading').get('data-total')
    page_size = ceil(int(total_products) / 36) * 36
    new_url = f'{url}?page-size={page_size}'
    
    return new_url

def get_main_data_of_products(soup):
    '''Returns a dataframe with main informations of products'''
    products = soup.find('ul', class_='products-listing small')

    products_list = products.find_all('article', class_='hm-product-item')
    # id
    product_id = [x.get('data-articlecode')for x in products_list]

    # category
    product_category = [x.get('data-category')for x in products_list]

    products_list = products.find_all('a', class_='link')

    # name 
    product_name = [product.text for product in products_list]

    products_list = products.find_all('span', class_='price regular')

    # price
    product_price = [product.text for product in products_list]
    
    # geting the time of webcraping
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # creating a dataframe
    data = pd.DataFrame({
        'product_id': product_id,
        'product_name':product_name,
        'product_category': product_category,
        'product_price': product_price,
        'scrapy_time': date_time
    })
    
    return data