import pandas as pd
import logging
import time

from jobs.hm import showcase_products as j1
from jobs.hm import detail_product as j2
from jobs.hm import cleaning as j3
from jobs.hm import database_insertion as j4

def hm_webscraping():
    logging.basicConfig(
        filename = 'Logs/webscraping_hm.log',
        level = logging.DEBUG,
        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger('webscraping_hm')

    url = 'https://www2.hm.com/en_us/men/products/jeans.html'


    headers = {"User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    ### JOB 01 --> showcase_products

    soup = j1.get_a_soup(url, headers)
    # the main link does not have all products
    new_url = j1.get_url_all_products(url, soup)
    soup_all_products = j1.get_a_soup(new_url, headers)

    df_products = j1.get_main_data_of_products(soup_all_products)
    logger.info('showcase collect done')


    ### JOB 02 --> detail_product

    df_charac = pd.DataFrame()

    for _id in df_products['product_id']:
        # dict with characteristics of a a single product
        dict_product = j2.get_characteristics_of_a_product(_id, headers)
        if dict_product:
            pass # code 200 --> no problem
        else:
            logger.debug(f'Product {_id} FAILED')
            time.sleep(1)
            continue   
        # appending
        df_charac = df_charac.append(dict_product, ignore_index=True)
        #logger.debug(f'Product {_id} collect done')
        time.sleep(1)

    df_webscrap = df_products.merge(df_charac, left_on='product_id', right_on='Art. No.')
    logger.info('product details collect done')

    ### JOB 03 --> cleaning

    data = j3.get_data_cleaning(df_webscrap)
    logger.info('data cleaning done')

    ### JOB 04 --> database_insertion 


    #j4.create_database()

    j4.append_database(data)
    logger.info('data insertion done')
