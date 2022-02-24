import requests
import time
from bs4 import BeautifulSoup
import json
import re


def get_a_soup(url, headers):
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    else:
        return False

def get_characteristics_of_a_product(id_, headers):
    '''returns a dict with characteristics of a a single product (you can use to append a dataframe)'''
    # getting a soup
    url = f'https://www2.hm.com/en_us/productpage.{id_}.html'
    soup = get_a_soup(url, headers=headers)
    if soup:
        pass # code 200 --> no problem
    else:
        return False

    
    # ===================== color ==============================
    colors = soup.find('ul', class_='inputlist clearfix')

    list_colors = colors.find_all('a')

    product_colors = [color.get('data-color') for color in list_colors if id_ == color.get('data-articlecode')]
    
    # ===================== other characteristics==============================

    characteristics = soup.find(class_='js-before-secondary-images').find('div')
    x = characteristics.find_all('script')[-1].text
    # cleaning 
    x = x.replace('\r', '').replace('\t', '').replace('\n', '').replace('\\"', '').replace("\\'","")

    # getting the data
    p = re.search('\[.*(s*{.*}s*).*\]', x).group(0)

    # needs to be " " to the json.loads work
    p = p.replace("'", '"')
    p = p.replace('title', '"title"')
    p = p.replace('values', '"values"')

    # json format
    json_data = json.loads(p)

    # ===================== creating a dict to return ==============================
    
    dict_product_characteristics = {}
    
    # adding to the return dict
    for line  in json_data:
        title = line['title']
        content = line['values']
        if len(content) == 1:
            content = content[0]
        dict_product_characteristics[title] = content

    dict_product_characteristics['product_color'] = product_colors #'|'.join(product_colors)
    
    return dict_product_characteristics