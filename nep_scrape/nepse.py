import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = 'https://merolagani.com/LatestMarket.aspx'


response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
   
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    table = soup.find('table', class_='table table-hover live-trading sortable')
    
    if table:
        
        headers = [header.text.strip() for header in table.find_all('th')]
        #print("Headers:", headers)
        data=[]
        
        rows = table.find_all('tr')[1:]  # Skipping the header row
        for row in rows:
           
            columns = row.find_all('td')
            if len(columns) >= 8:  
                stock_symbol = columns[0].text.strip()  # Stock symbol is in the first column
                pclose_price = columns[5].text.strip()
                Percentage_change= columns[2].text.strip()
                #print(f"Stock: {stock_symbol}, PClose: {pclose_price} , Percentage_change: {Percentage_change}")
                
                data.append([stock_symbol, pclose_price, Percentage_change] )
                 # Create a DataFrame
        df = pd.DataFrame(data, columns=['Stock Symbol', 'PClose', 'Percentage_change'])
        
        # Save the DataFrame to a CSV file
        df.to_csv('stock_prices.txt', index=False, sep='\t')
        
        print("Data saved to stock_prices.txt")
    else:
        print("Couldn't find the table containing stock prices.")
else:
    print(f"Failed to retrieve webpage: {response.status_code}")
