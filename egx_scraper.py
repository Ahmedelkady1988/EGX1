
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_tag = soup.find("span", {"data-test": "instrument-price-last"})
        price = float(price_tag.text.replace(",", "")) if price_tag else None
        return price
    except Exception as e:
        return None

# Load the stock list
df = pd.read_excel("Stocks Links.xlsx", sheet_name="Stocks")

# Loop over each URL
results = []
for i, row in df.iterrows():
    url = row["URL"]
    price = fetch_data(url)
    results.append({
        "Company": row["Company Name"],
        "Code": row["Code"],
        "Price": price,
        "Sector": row["Sector"]
    })

# Save to CSV
df_result = pd.DataFrame(results)
df_result.to_csv("egx_data.csv", index=False)
print("Updated egx_data.csv:", datetime.now())
