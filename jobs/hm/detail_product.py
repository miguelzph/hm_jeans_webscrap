import requests
import time
from bs4 import BeautifulSoup


def get_a_soup(url, headers, tentatives=5):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    return soup

def get_characteristics_of_a_product(id_, headers):
    '''returns a dict with characteristics of a a single product (you can use to append a dataframe)'''
    # getting a soup
    url = f'https://www2.hm.com/en_us/productpage.{id_}.html'
    soup = get_a_soup(url, headers=headers)

    # ===================== color ==============================
    colors = soup.find('ul', class_='inputlist clearfix')

    list_colors = colors.find_all('a')

    product_colors = [color.get('data-color') for color in list_colors if id_ == color.get('data-articlecode')]
    
    # ===================== other characteristics==============================

    characteristics = soup.find('div', class_='content pdp-text pdp-content')
    characteristics_list = characteristics.find_all('div', class_='pdp-description-list-item')

    # title of characteristics
    characteristics_title = [char.find('dt').text for char in characteristics_list]

    # characteristics
    # getting the data
    characteristics = [char.find_all(['li','dd']) for char in characteristics_list]
    # cleaning the data -- > x is a list
    characteristics = [x if len(x)==1 else x[1:] for x in characteristics]
    # transforming the data --> x is a list // y is a value of a list x
    characteristics = [x[0].text if len(x)==1 else [y.text for y in x] for x in characteristics]

    # ===================== creating a dict to return ==============================

    dict_product_characteristics = {characteristics_title[i]: characteristics[i] for i in range(len(characteristics))}
    dict_product_characteristics['product_color'] = product_colors #'|'.join(product_colors)
    
    return dict_product_characteristics