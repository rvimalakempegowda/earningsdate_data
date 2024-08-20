import pandas as pd
from datetime import datetime, timedelta
import os

# Load the AMD financial data from the provided CSV file
file_path = 'AMD.csv'  # Update with the correct path to your file

# Ensure the file exists
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

data = pd.read_csv(file_path)

# Convert the date column to datetime format (assuming format is YYYY-MM-DD)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

# Ensure data is sorted by date
data = data.sort_values(by='Date')

# Function to extract exactly 30 data points before the earnings date
def extract_30_data_points(earning_date):
    try:
        # Convert the input earnings date to a datetime object
        earning_date = datetime.strptime(earning_date, '%d-%m-%Y')
    except ValueError:
        raise ValueError("The earnings date must be in the format dd-mm-yyyy.")
    
    # Filter data to get all entries before the earnings date
    filtered_data = data[data['Date'] < earning_date]
    
    # Check if we have at least 30 entries
    if len(filtered_data) < 30:
        raise ValueError("Not enough data points available before the earnings date.")
    
    # Get the last 30 data points
    last_30_days_data = filtered_data.tail(30)
    
    # Convert dates to the desired format
    last_30_days_data['Date'] = last_30_days_data['Date'].dt.strftime('%d-%m-%Y')
    
    return last_30_days_data

# Input the earnings date
earning_date = input("Enter the earnings date (dd-mm-yyyy): ")

# Extract the last 30 data points before the earnings date
try:
    last_30_days_data = extract_30_data_points(earning_date)
except ValueError as e:
    print(e)
    exit()

# Output the extracted data to a new Excel file
output_file_path = '16102001.xlsx'
last_30_days_data.to_excel(output_file_path, index=False)

print(f"Extracted data has been saved to {output_file_path}")
