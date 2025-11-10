# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from datetime import datetime

date_format = '%d/%m/%Y'

systembook = pd.read_csv('03_Library Systembook.csv')


#create the Book data frame
def create_book_df(systembook):
    Books_df = systembook['Books']
    
    Books_df = pd.DataFrame(Books_df.drop_duplicates().dropna())
    
    Books_df['Book_id'] = range(1,len(Books_df)+1)
    
    return Books_df

Books = create_book_df(systembook)



def is_date_valid(date_str, date_format = '%d/%m/%Y'):
    try:
        #date_str.str.strip().str.replace('"', '')
        #datetime.strptime(date_str, date_format)
        datetime.strptime(date_str.strip('"'), date_format)
        return True
    except ValueError:
        return False
    
    
systembook['Book checkout clean'] = systembook['Book checkout'].astype(str).str.strip().str.replace('"', '')
systembook['Book checkout valid'] = systembook['Book checkout clean'].apply(lambda x: is_date_valid(x))
systembook['Book checkout valid'] = systembook['Book checkout valid'].astype(bool)
    
systembook['Book Returned clean'] = systembook['Book Returned'].astype(str).str.strip().str.replace('"', '')
systembook['Book Returned valid'] = systembook['Book Returned clean'].apply(lambda x: is_date_valid(x))
systembook['Book Returned valid'] = systembook['Book Returned valid'].astype(bool)#BookRentals = systembook[systembook['Book Returned valid']] and systembook[systembook['Book checkout valid']].copy()

# new_df = df.loc[(df.col1 == True) & (df.col2==True),]
# errors = df.loc[df.col1 == False]

BookRentals = systembook.loc[(systembook['Book Returned valid'] ==True) & (systembook['Book checkout valid'] ==True)]

BookRentals_exception = systembook.loc[(systembook['Book Returned valid'] ==False) | (systembook['Book checkout valid'] ==False)]