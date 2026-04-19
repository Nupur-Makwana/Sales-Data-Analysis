# -*- coding: utf-8 -*-
"""

@author: nupur
"""

import pandas as pd
import os

# Get all files
files = [file for file in os.listdir('../data/Sales_Data')]

all_month_data = pd.DataFrame()

# Combine all months
for file in files:
    df = pd.read_csv("../data/Sales_Data/" + file)
    all_month_data = pd.concat([all_month_data, df])

# Save combined data
all_month_data.to_csv("../data/all_data.csv", index=False)

# Read combined file
all_data = pd.read_csv("../data/all_data.csv")

# Clean data
all_data = all_data.dropna(how='all')
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

# Convert types
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

# Add Month
all_data['Month'] = all_data['Order Date'].str[0:2].astype('int32')

# Add Sales
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

# Add City
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(
    lambda x: f"{get_city(x)} ({get_state(x)})"
)

# Save cleaned data
all_data.to_csv("../data/cleaned_sales_data.csv", index=False)

print("Cleaned Data Saved")