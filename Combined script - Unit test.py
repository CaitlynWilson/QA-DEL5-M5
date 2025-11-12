# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:47:35 2025

@author: Admin
"""

#import unittest
#from calculator_app import Calculator

# class TestOperations(unittest.TestCase):

#     def test_sum(self):
#         calc = Calculator(2,8)
#         self.assertEqual(calc.get_sum(), 10, "The sum is wrong")

# if __name__ == "__main__":
#     unittest.main()        

import unittest
from combined_script import open_file
from combined_script import duplicate_drop
from combined_script import is_date_valid
import pandas as pd


class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        
        self.df = pd.DataFrame({'A':[1,1],'B':[3,3],'C': [5,5]})
        self.date_format = '%d/%m/%Y'
    
    def test_open_file(self):
        self.test_csv = r'C:\Users\Admin\Desktop\QA-DEL5-M5\Unit testing\test.csv'
        pd.DataFrame({'A':[1,1],'B':[3,3],'C': [5,5]}).to_csv(self.test_csv, index=False)
        pd.testing.assert_frame_equal(open_file(self.test_csv), self.df)
        
    def test_drop_duplicates(self):
        expected = pd.DataFrame({'A':[1],'B':[3],'C':[5]})
        pd.testing.assert_frame_equal(duplicate_drop(self.df), expected)
        
    def test_is_date_valid(self):
        valid_date_string = '"01/01/2025"'
        valid_expected = True
        
        invalid_date_string = '30/02/2025"'
        invalid_expected = False
        
        self.assertEqual(is_date_valid(valid_date_string, self.date_format) , valid_expected)
        self.assertEqual(is_date_valid(invalid_date_string, self.date_format), invalid_expected)
        
        
            
        
                
        

if __name__ == "__main__":
    unittest.main()
       