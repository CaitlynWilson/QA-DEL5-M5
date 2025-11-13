# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 10:44:18 2025

@author: Admin
"""

import pandas as pd
#from datetime import datetime
#import numpy as np
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



  
def date_cleanser(col, df): 
    df[col] = df[col].str.replace('"', '')

    df[col] = pd.to_datetime(df[col], dayfirst=True, errors = 'coerce').dt.date
    
    col_name = f'{col}_flag'
    df[col_name] = df[col].notnull().astype(int)
    
    #df_exception = df.loc[]
    
    #df_exception = df.loc[]
    
    return df    

def date_exception(df, flag1, flag2):
    df_main = df.loc[(df[flag1] == 1) & (df[flag2] == 1)]
    df_exception = df.loc[(df[flag1] == 0) | (df[flag2] == 0)]
    return df_main, df_exception

def days_borrowed(col1, col2, df):
    df['DaysBorrowed'] = (col1 - col2).apply(lambda x: x.days)
    df['DaysBorrowed'] = df['DaysBorrowed'].astype(int)
    df_main = df.loc[(df['DaysBorrowed'] >= 0)]
    df_exception = df.loc[(df['DaysBorrowed'] < 0)]
    return df_main, df_exception   

def weeks_to_days(col):
    if isinstance(col, str) and 'week' in col:
        num_week = int(col.split()[0])
        col = num_week * 7
        return col
    else:
        return col
    return col


def write_to_sql(BooksRented, BooksRented_exception, Customers):
    
    #setting up SQL db params
    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LibraryDB;Trusted_Connection=yes;")

    #create engine to connect
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    
    BooksRented.to_sql('BooksRented', con=engine, if_exists='append', index=False)
    BooksRented_exception.to_sql('BooksRented_exception', con=engine, if_exists='append', index=False)
    Customers.to_sql('Customers', con=engine, if_exists='append', index=False)

def main():
    #Books
    filepath = './Data_raw/03_Library Systembook.csv'
    BooksRented = open_file(filepath)
    
    #drop records with duplicates other than the first ID field
    BooksRented = drop_duplicates(BooksRented)
    
    #fill str with unknown rather than dropping
    BooksRented = BooksRented.apply(na_fill)
    
    #drop records with nulls
    BooksRented = drop_na(BooksRented)
    
    #list date fields
    date_columns = ['Book checkout', 'Book Returned']
    
    #change str to date and create error flag
    for col in date_columns:
        BooksRented = date_cleanser(col, BooksRented)
    
    
    #def cleansed_csv():
    #create exception table and main table
    BooksRented,BooksRented_exception =  date_exception(BooksRented,'Book checkout_flag', 'Book Returned_flag')
    
    #calculate the daysborrowed field, any negative daysborrowed move to another exception table
    BooksRented, BooksRented_exception2 = days_borrowed(BooksRented['Book checkout'],BooksRented['Book Returned'], BooksRented)
    
    #concat the two exceptions together 
    BooksRented_exception = pd.concat([BooksRented_exception, BooksRented_exception2], ignore_index=True )
    
    #change weeks to days
    BooksRented['Days allowed to borrow'] = BooksRented['Days allowed to borrow'].apply(lambda x:weeks_to_days(x))
    
    #drop unwanted fields
    BooksRented = BooksRented.drop(columns = {'Book checkout_flag','Book Returned_flag' })
    
    #saving as csv
    BooksRented.to_csv('./Data_cleansed/BooksRented.csv', index = False)
    BooksRented_exception.to_csv('./Data_cleansed/BooksRented_exception.csv', index = False)
    
    
    
    #customer
    filepath = './Data_raw/03_Library SystemCustomers.csv'
    Customers = open_file(filepath)
    
    #drop duplicates
    Customers = drop_duplicates(Customers)
    
    #drop na
    Customers = drop_na(Customers)
    
    #save as csv
    Customers.to_csv('./Data_cleansed/Customers')
    
    #call the write_to_sql function to make df a sql table
    write_to_sql(BooksRented, BooksRented_exception, Customers)

    

if __name__ =="__main__":
    
    
    main()