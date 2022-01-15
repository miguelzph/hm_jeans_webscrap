import pandas as pd
import re

def get_data_cleaning(df):  
        
    # lower the name of columns 
    df.columns = df.columns.to_series().apply(lambda x: x.replace(' ', '_').lower())
    # exploding a column --> create a new line to each value in a list
    df = df.explode('composition')

    # ===================== product_id ===================== --> nothing to do

    # ===================== product_price =====================
    df['product_price'] = df['product_price'].apply(lambda x: x.replace('$ ','')).astype(float)

    # ===================== product_name =====================
    df['product_name'] = df['product_name'].apply(lambda x: x.replace(' ', '_').lower())

    # =====================product_category ===================== --> nothing to do

    # ===================== scrapy_time ===================== --> nothing to do

    # ===================== art._no. =====================
    # same values as product_id
    df = df.drop(columns=['art._no.'])

    # ===================== composition =====================
    # creating a column to link each part with the respective composition
    # gets the name before ":" in there's no ":" --> go to "shell"
    df['composition_type'] = df['composition'].apply(lambda x: re.search('(.+): ', x).group(1) if ': ' in x
                                                        else 'shell')
    df['composition_type'] = df['composition_type'].apply(lambda x: x.replace(' ','_').lower())

    # pocket lining or lining or shell will be considered as a composition type --> remove all before ": "
    df['composition'] = df['composition'].apply(lambda x: re.search(': (.+)', x).group(1) if ': ' in x
                                                   else x)

    # creating a column to each element
    composition_elements = ['Cotton', 'Spandex', 'Polyester', 'Elasterell-P']
    for element in composition_elements:
        df[element] = df['composition'].apply(
            lambda x: float(re.search(f'{element} (\d+)%', x).group(1)) / 100
            if element in x else 0.00)

    df.columns = df.columns.to_series().apply(lambda x: x.replace('-', '_').lower())
    # removing the composition column
    df = df.drop(columns=['composition'])

    # ===================== fit =====================
    df['fit'] = df['fit'].apply(lambda x: x.replace(' ','_').lower() if x==x else x)

    # ===================== size =====================
    # creating size_number
    df['size_number'] = df['size'].apply(lambda x: int(re.search('(\d{3})cm', x).group(1)) if pd.notnull(x) else x) 

    # creating size_model
    df['size_model'] = df['size'].apply(lambda x: re.search('size (.+)', x).group(1) if pd.notnull(x) else x) 

    # deleting size
    df = df.drop(columns=['size'])

    # ===================== product_color =====================
    df['product_color'] = df['product_color'].apply(lambda x: x[0].replace(' ','_').lower())

    # ===================== more_sustainable_materials =====================
    # almost full of NaN's
    if 'product_safety' in df.columns:     
        df = df.drop(columns=['product_safety'])

    # ===================== product_safety =====================
    # adapting a column to yes / no dependes if there's recycle material or no
    if 'more_sustainable_materials' in df.columns:   
        df['recycled_material'] = df['more_sustainable_materials'].apply(lambda x: 'yes' if x==x else 'no')
    else:
        df['recycled_material'] = 'no'
    df = df.drop(columns=['more_sustainable_materials'])
    
    return df