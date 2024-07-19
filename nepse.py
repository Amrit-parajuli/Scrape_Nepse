import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')

@app.route('/')
def scrape_stocks():
    url = 'https://merolagani.com/LatestMarket.aspx'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-hover live-trading sortable')
        
        if table:
            headers = [header.text.strip() for header in table.find_all('th')]
            data = []
            
            rows = table.find_all('tr')[1:]  # Skipping the header row
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 8:  
                    stock_symbol = columns[0].text.strip()  # Stock symbol is in the first column
                    pclose_price = columns[5].text.strip()
                    percentage_change = columns[2].text.strip()
                    # Append data to the list
                    data.append([stock_symbol, pclose_price, percentage_change])
            
            # Create a DataFrame
            df = pd.DataFrame(data, columns=['Stock Symbol', 'PClose', 'Percentage Change'])
            
            # Convert DataFrame to JSON
            json_data = df.to_dict(orient='records')
            return jsonify(json_data)
        else:
            return jsonify({"error": "Couldn't find the table containing stock prices."})
    else:
        return jsonify({"error": f"Failed to retrieve webpage: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
