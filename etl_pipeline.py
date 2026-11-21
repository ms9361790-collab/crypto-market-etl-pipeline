import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# 1. EXTRACT: CoinGecko API se Top 10 Crypto ka data (INR mein)
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "inr",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()
data = response.json()

# 2. TRANSFORM: Pandas se data clean aur format karein
df = pd.DataFrame(data)[[
    "name", "symbol", "current_price", "market_cap", "price_change_percentage_24h"
]]

df["symbol"] = df["symbol"].str.upper()
df["price_change_percentage_24h"] = df["price_change_percentage_24h"].round(2)
df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. LOAD: SQLite Database aur CSV mein save karein
conn = sqlite3.connect("crypto_market.db")
df.to_sql("daily_prices", conn, if_exists="append", index=False)
conn.close()

df.to_csv("latest_market_data.csv", index=False)

# 4. VISUALIZE: 24h % Change ka Bar Chart banayein
plt.figure(figsize=(10, 5))
colors = ["green" if x >= 0 else "red" for x in df["price_change_percentage_24h"]]
plt.bar(df["symbol"], df["price_change_percentage_24h"], color=colors)
plt.axhline(0, color="black", linewidth=0.8)
plt.title(f"Top 10 Crypto - 24h Price Change (%) | {datetime.now().strftime('%d %b %Y')}")
plt.xlabel("Cryptocurrency")
plt.ylabel("24h Change (%)")
plt.tight_layout()
plt.savefig("daily_chart.png")
plt.close()

print("ETL Pipeline successfully completed!")
print(df[["symbol", "current_price", "price_change_percentage_24h"]])
