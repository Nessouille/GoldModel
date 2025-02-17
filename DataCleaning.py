import pandas as pd
import numpy as np
from LoggerConfig import logger
from spicy.stats import zscores
import sklearn.preprocessing as skp
from sklearn.model_selection import train_test_split

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
#Handle outliers using IQR or Z scores
#Scale data using standard, robust or minmax scaling
#Feature selection
#Split data in trainning and testing sets
#Create data sets with raw data, feature selected data, and outlier removed data
#Data should be ready to be handled by any supervised or unsupervised learning algorythm in Model.py
class DataPreprocess:
    def __init__(self,df):
        self.df = df

    def remove_outliers(self, methods = 'zscores', threshold = 3):
        #Make a copy of the data frame with and without outliers
        df_out = self.df.copy()
        df_with = self.df.copy()
        logger.info("data frame copies created")
        numerical_cols = df_out.select_dtypes(include = np.number).columns

        #Implement Z score calculation (z = (X – μ) / σ) and removal of outliers
        if methods == 'zscores':
            z_scores = df_out[numerical_cols].apply(zscores)
            mask = (z_scores < threshold) & (z_scores> -threshold)
            df_out = df_out[mask.all(axis=1)]
            logger.info("Z_scores method applied. Outlier removed")


        #Implement IQR calculations (Q3 -Q1) and removal of outliers (tolerance of 1.5)
        elif methods == 'IQR':
            Q1 = df_out[numerical_cols].quantile(0.25)
            Q3 = df_out[numerical_cols].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 - (1.5 * IQR)
            mask = (df_out[numerical_cols]>= lower_bound) & (df_out[numerical_cols]<= upper_bound)
            df_out = df_out[mask.all(axis=1)]
            logger.info("IQR method applied. Outlier removed")

            return df_out, df_with
    
    def scale_features(self,df, method = 'standard'):
        #Allows the user to pick which dataFrame they want to use from the remove_outlier method and create a copy before scaling
        df_scaled = df.copy()
        #Select numerical columns only for scaling
        numerical_cols = df_scaled.select_dtypes(include = np.number).columns
        #Scaling techniques available: standard, robust, minmax
        #Standardise data (mean = 0, standard deviation = 1)
        if method == 'standard':
            scaler = skp.StandardScaler()
        #Robust scaling (median = 0, IQR = 1)
        elif method == 'Robust':
            scaler = skp.RobustScaler()
        #Min max scaling (0 to 1) 
        elif method == 'MinMax':
            scaler = skp.MinMaxScaler()
            
        df_scaled[numerical_cols] = scaler.fit_transform(df_scaled[numerical_cols])
        logger.info("Scaling Complete using {}".format(method))

        return df_scaled
    
    def Split_data(self,df_scaled,target_column, test_size = 0.3):
        #Split data in trainning and testing sets
        X = self.df_scaled.drop(columns =[target_column],axis = 1)
        y = self.df_scaled[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = test_size, random_state = 42)

        logger.info(f"Trainning set:{X_train.shape}, Testing set = {X_test.shape}")

        return X_train, X_test, y_train, y_test

