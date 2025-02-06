import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
import logging

def main():
    logger.info('Script started')


logger = logging.getLogger(__name__)
# CLASS DEFINITION: FetchData
#Initialize the class with base_url and timeout.
#Dynamically pass endpoint to the fetch_data method.
#Combine base_url and endpoint to construct the full URL.
#Make the GET request and handle any exceptions.
#Return the HTML response (response.text)
class FetchStrategy:
    def __init__(self,base_url=None, timeout=5):
        self.base_url = base_url or "https://finance.yahoo.com"
        self.timeout = timeout
    def fetchData(self,endpoint=None):
        endpoint = endpoint or "/quote/GC=F" 
        try:
            #Dynamically create the URL
            url = f"{self.base_url.rstrip('/')}{endpoint.lstrip('/')}"
            #GET request with the timeout included
            response = requests.get(url,self.timeout)
            return response.text
        except requests.exceptions.Timeout:
            logger.exception(f"Request timed out after {self.timeout} seconds.")
        except requests.exceptions.RequestException as e:
            logger.exception(f"An error has occurred: {e}")

#CLASS DEFINITION ParseData
#Found the table
#Extracted rows
#Checked that rows have the correct number of cells
# Extract text from cells
# Convert data into pandas Dataframes
class ParseData:
    def __init__(self,response, columns=None, selector=None, soup=None):
        self.response = response
        self.columns = columns if columns else ['Date', 'Close', 'Open', 'Volume','High','Low']
        self.selector = selector or 'table[data-test="historical-prices"]'
    
    def parse_data(self):
        self.soup = bs(self.response, 'html.parser')
        table = self.soup.select_one(self.selector)
        if not table:
            logger.error("No table found in parsed HTML")
            return None
        logger.info("Table found")

        #Extract rows from table
        rows = table.find_all('tr')

        #Error logging for no rows
        if not rows:
            logger.error("No rows found")
            return None
        logger.info("Rows found")
        data = []
        for row in rows:
            cells = row.find_all('td')
            if not cells or len(cells) != len(self.columns):
                logger.info(f"Row has {len(cells)} cells. Expected {len(self.columns)}")
                continue
            data.append([cell.get_text(strip=True) for cell in cells]) #Extract and process data from HTML into the data list
            
            # Error logging for no data
            if not data: 
                logger.error("No data found")
                return None
            
        df=pd.Dataframe(data, columns=self.columns) #Create panda Dataframe from extracted and processed HTML data
        logger.info(f"Dataframe created with {len(df.shape[0])}")
        return df



#CLASS DEFIINITION 
if __name__ == '__main__':
    main()
    logging.getLogger(__name__)
    logging.setLevel(logging.DEBUG)
    
