import pandas as pd
from datetime import datetime


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