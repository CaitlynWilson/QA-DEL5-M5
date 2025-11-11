import pandas as pd
#from datetime import datetime
#import numpy as np
#import logging
from Functions import open_file
#from Functions import duplicate_drop
#from Functions import create_book_df
#from Functions import is_date_valid
#from Functions import date_cleanse
#from Functions import date_transformation
from Functions import is_na_check
from Functions import is_duplicate_check
#import week_to_days



##customers 
#load the csv as a dataframe
customers = open_file(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_raw\03_Library SystemCustomers.csv')

#check if is_na values
customers['is_na'] = is_na_check(customers)    

#check if is_dup values
customers['is_dup'] = is_duplicate_check(customers)

#Moving any duplicates or na values to exceptions
customers_exception = customers.loc[(customers['is_na'] ==True) | (customers['is_dup'] ==True)]

#keeping only valid customers
customers = customers.loc[(customers['is_na'] ==False) & (customers['is_dup'] ==False)]

customers = customers.drop(columns={'is_na', 'is_dup'})

#saving df as csv
customers.to_csv(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_cleansed\customers.csv', index =False)
customers_exception.to_csv(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_cleansed\customers_exception.csv', index =False)