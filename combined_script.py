import pandas as pd
from datetime import datetime
import numpy as np
import logging

def open_file(csv_file):
    df = pd.read_csv(csv_file)
    return df



def duplicate_drop(df):
    df_dedupe = df.drop_duplicates()
    return df_dedupe

#create the Book data frame
def create_book_df(systembook):
    Books_df = systembook['Books']
    Books_df = pd.DataFrame(Books_df)
    #Books_df = pd.DataFrame(Books_df.drop_duplicates().dropna())
    Books_df = duplicate_drop(Books_df)
    Books_df['Book_id'] = range(1,len(Books_df)+1)
    return Books_df



def is_date_valid(date_str, date_format = '%d/%m/%Y'):
    try:
        #date_str.str.strip().str.replace('"', '')
        #datetime.strptime(date_str, date_format)
        datetime.strptime(date_str.strip('"'), date_format)
        return True
    except ValueError:
        return False
    

def date_cleanse(original_date):
    strip_date = original_date.astype(str).str.strip().str.replace('"', '')
    date_valid = strip_date.apply(lambda x: is_date_valid(x))
    return strip_date, date_valid
     
def date_transformation(date_str):
     date = pd.to_datetime(date_str, format ='mixed').dt.date
     #date = date.strftime('%d/%m/%Y')
     return date   


def is_na_check(df):
    na_check = df.iloc[:,1:].isna().any(axis=1)
    return na_check     


def is_duplicate_check(df):
    dup_check =df.duplicated(df.iloc[:,1:], keep='first')
    return dup_check

def week_to_days(value):
    if isinstance(value, str) and 'week' in value:
        num_weeks = int(value.split()[0])
        value = num_weeks * 7
        return value
    else: 
        return value
    return value
        

#load the csv's as dataframes
systembook = open_file(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_raw\03_Library Systembook.csv')
logging.info('Systembook csv open successfully')
Books = create_book_df(systembook)

#update na value to 'Unknown' in books
Books['Books'] = Books['Books'].replace(np.nan, 'Unknown Title')

##Book and BookedRentals 
#clean and validate the dates
systembook['Book checkout clean'], systembook['Book checkout valid'] = date_cleanse(systembook['Book checkout'])
systembook['Book Returned clean'], systembook['Book Returned valid'] = date_cleanse(systembook['Book Returned'])


#create the main table where dates are a valid format
BookRentals = systembook.loc[(systembook['Book Returned valid'] ==True) & (systembook['Book checkout valid'] ==True)]

#create the exceptions table
BookRentals_exception = systembook.loc[(systembook['Book Returned valid'] ==False) | (systembook['Book checkout valid'] ==False)]

#change the valid dates to date format
BookRentals['Book checkout clean'] = date_transformation(BookRentals['Book checkout clean'])
BookRentals['Book Returned clean'] = date_transformation(BookRentals['Book Returned clean'])

#calculating the number of days borrowed
BookRentals['DaysBorrowed'] = (BookRentals['Book Returned clean'] - BookRentals['Book checkout clean']).apply(lambda x: x.days)

#checking if any na values exist
BookRentals['is_na'] = is_na_check(BookRentals)

#check if any duplicates exist
BookRentals['is_dup'] = is_duplicate_check(BookRentals)


#if days borrowed is negative, move them into the exceptions table
exceptions_tmp = BookRentals.loc[(BookRentals['DaysBorrowed'] < 0) | (BookRentals['is_na'] ==True) | (BookRentals['is_dup'] ==True)]
BookRentals_exception = pd.concat([BookRentals_exception, exceptions_tmp], ignore_index=True)
BookRentals = BookRentals.loc[(BookRentals['DaysBorrowed'] >= 0) & (BookRentals['is_na'] ==False) & (BookRentals['is_dup'] ==False)]



#drop columns that aren't needed
BookRentals = BookRentals.drop(columns = ['Book checkout valid', 'Book Returned valid', 'Book checkout','Book Returned','is_na', 'is_dup'])

#rename columns
BookRentals = BookRentals.rename(columns={'Book checkout clean': 'Book checkout','Book Returned clean': 'Book Returned'})

#changing weeks to days
BookRentals['Days allowed to borrow'] = BookRentals['Days allowed to borrow'].apply(lambda x: week_to_days(x))

#saving df as csv
Books.to_csv(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_cleansed\Books.csv', index =False)
BookRentals.to_csv(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_cleansed\BookRentals.csv', index =False)
BookRentals_exception.to_csv(r'C:\Users\Admin\Desktop\QA-DEL5-M5\Data_cleansed\BookRentals_exception.csv', index =False)


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