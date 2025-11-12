# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 10:44:18 2025

@author: Admin
"""

import pandas as pd
from datetime import datetime
import numpy as np
import logging
from sqlalchemy import create_engine
import urllib


    

def open_file(filepath):
    df = pd.read_csv(filepath)
    return df


def drop_duplicates(df):
    #df.duplicated(df.iloc[:,1:], keep='first')
    df['is_dup'] = df.duplicated(df.iloc[:,1:], keep='first')
    df = df.loc[(df['is_dup'] ==False)]
    df = df.drop('is_dup', axis = 1)
    return df 

def na_fill(col):
    if col.dtypes == 'object':
        return col.fillna('Unknown')
    else:
        return col
    
def drop_na(df):
    df = df.dropna()
    return df


def date_cleanser(date_columns, df):
    #date_format = '%d/%m/%Y'
    for col in date_columns:
        def is_date_valid(col):
            try:
                col_clean = str(col).strip('"').strip("'").strip()
                datetime.strptime(col_clean.strip('"'), '%d/%m/%Y')
                return True
            except Exception:
                return False
        df[f'{col}_is_valid'] = df[col].apply(is_date_valid)
        valid_col = df[f'{col}_is_valid']
      
        def date_transformation(col, valid_col):
            if valid_col ==True:
                
                col = pd.to_datetime(col, dayfirst=True).dt.date
                return col
            else:
                return col
        
        date_transformation(col,valid_col)    
    return df  
        
         

    


filepath = r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_raw\\03_Library Systembook.csv'
BooksRented = open_file(filepath)

#drop records with duplicates other than the first ID field
BooksRented = drop_duplicates(BooksRented)

#fill str with unknown rather than dropping
BooksRented = BooksRented.apply(na_fill)

#drop records with nulls
BooksRented = drop_na(BooksRented)

date_columns = ['Book checkout', 'Book Returned']

BooksRented = date_cleanser(date_columns, BooksRented)




