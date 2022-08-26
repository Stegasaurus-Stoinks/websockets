import pandas as pd
import time

data = pd.read_csv(r'C:\Users\pwild\Documents\Projects\Stega-Stoinks\websockets\Polygon-Alpaca-API\class restructuring\BTCUSDminute1.csv')

# Preview the first 5 lines of the loaded data 
print(data.head())

if 0:
	for i, row in data.iterrows():
		print(f"Index: {i}")
		print(f"{row['open']}")
		time.sleep(1)