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
    url = "https://www.sharesansar.com/today-share-price"

# Send a GET request to fetch the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    
    # Locate the table
        table = soup.find("table", id="headFixed")
    
  
        if table:
        
            rows = table.find("tbody").find_all("tr")
            data = []
            for row in rows:
                cells = row.find_all("td")
            
            
                if len(cells) > 8:
                    prev_close = cells[9].text.strip()
                    stock_symbol=cells[1].text.strip()
                    percentage_change=cells[14].text.strip()
                    data.append([stock_symbol, prev_close, percentage_change])
            
            # Create a DataFrame
            df = pd.DataFrame(data, columns=['Stock_Symbol', 'PClose', 'Percentage_Change'])
            
            # Convert DataFrame to JSON
            json_data = df.to_dict(orient='records')
            return jsonify(json_data)
        else:
            return jsonify({"error": "Couldn't find the table containing stock prices."})
    else:
        return jsonify({"error": f"Failed to retrieve webpage: {response.status_code}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
