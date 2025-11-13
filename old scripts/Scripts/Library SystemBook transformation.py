# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
#from datetime import datetime
import numpy as np
import logging
from Functions import open_file
#from Functions import duplicate_drop
from Functions import create_book_df
#from Functions import is_date_valid
from Functions import date_cleanse
from Functions import date_transformation
from Functions import is_na_check
from Functions import is_duplicate_check
from Functions import week_to_days

        

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


