import pandas as pd
import numpy as np
from LoggerConfig import logger

#CLASS DEFINITION DataFormatter
#Ensure the data types are correct 
#Handle missing values or outliers
#Convert any necessary columns 
#Optionally, normalize/scale data if needed
class DataFormatter:
    def __innit__(self,df):
        self.df = df
    
    def clean_data(self):
        logger.info("Cleaning data: start")
        #date to datetime converion, if not possible set date to NaT (Not a time)
        self.df['Date'] = pd.to_datetime(self.df['Date'], errors = 'coerce') 
        #All other numerical columns are converted to numeric, if not possible convert to NaN
        for col in ['Close', 'Open', 'Volume', 'High', 'Low']:
            self.df[col] = pd.to_numeric(self.df[col], errors = 'coerce')
        
        #Implemant data manipulation strategies
        #Forward fill (carry over in time series)
        self.df.fillna(methods='ffill', inplace ='True')

        #Backward fill first row if missing data
        self.df.fillna(methods = 'bfill', max = 1, inplace ='True')

        #Linear interpolation of large gaps in data 
        self.df.interpolate(methods = 'linear', interpolate = 'True')

        #Handle large data gaps (more than 5 missign values in a row) with a median interpollation
        if self.df['Close'].isna().sum() > 5:
            self.df['Close'] = self.df['Close'].fillna(self.df['Close'].median(), inplace = 'True')
        
        logger.info("Cleaning data: complete")

        return self.df
    
#CLASS DEFINITION DataPreprocess
#Handle outliers
#Scale data
#Feature selection
#Split data in trainning and testing sets
#Create data sets with raw data, feature selected data, and outlier removed data
#Data should be ready to be handled by any supervised or unsupervised learning algorythm in Model.py
class DataPreprocess:
    def __innit__(self,df):
        self.df = df