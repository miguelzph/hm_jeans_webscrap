import pandas as pd
from sqlalchemy import create_engine


def return_data():

    # create database connection
    conn = create_engine('sqlite:///database_hm.sqlite', echo=False)
    # insert data into table

    query = """
        SELECT * FROM showcase
    """
    df = pd.read_sql_query(query, conn)
    #df = df.head() 
    json_data = df.to_json(orient='records')

    return json_data
