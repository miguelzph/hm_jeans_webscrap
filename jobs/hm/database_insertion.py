import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def select_columns(data):
    data_insert = data[[
        'product_id', 
        'product_name',
        'product_color',
        'product_price',
        'product_category',
        'fit', 
        'composition_type', 
        'cotton',
        'spandex',
        'polyester', 
        'elasterell_p',
        'recycled_material',
        'size_number', 
        'size_model',
        'scrapy_time'
    ]]

    return data_insert

def create_database():
    query_create_table = """
    CREATE TABLE showcase(
    product_id TEXT,
    product_name TEXT,
    product_color TEXT,
    product_price REAL,
    product_category TEXT,
    fit TEXT,
    composition_type TEXT, 
    cotton REAL,
    spandex REAL,
    polyester REAL,
    elasterell_p REAL,
    recycled_material TEXT,
    size_number REAL,
    size_model TEXT,
    scrapy_time TEXT
    )
    """

    conn = sqlite3.connect('database_hm.sqlite')
    cursor = conn.execute(query_create_table)
    conn.commit()
    conn.close()

    return None


def append_database(data):
    data_insert = select_columns(data)
    
    # create database connection
    conn = create_engine('sqlite:///database_hm.sqlite', echo=False)
    # insert data into table
    data_insert.to_sql( 'showcase', con=conn, if_exists='append',index=False ) 

    return None
