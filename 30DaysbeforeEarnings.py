import pandas as pd
from datetime import datetime, timedelta
import os

# Function to extract the last 30 data points before the earnings date
def extract_30_data_points(data, earning_date):
    filtered_data = data[data['Date'] < earning_date]
    if len(filtered_data) < 30:
        raise ValueError("Not enough data points available before the earnings date.")
    last_30_days_data = filtered_data.tail(30)
    last_30_days_data['Date'] = last_30_days_data['Date'].dt.strftime('%d-%m-%Y')
    return last_30_days_data

# Load the AMD financial data
file_path = 'AMD.csv'  # Update with the correct path to your file
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

data = pd.read_csv(file_path)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data = data.sort_values(by='Date')

earnings_dates = [
    '17-01-2001', '18-04-2001', '12-07-2001', '17-10-2001',
    '16-01-2002', '17-04-2002', '17-07-2002', '16-10-2002',
    '16-01-2003', '16-04-2003', '16-07-2003', '16-10-2003',
    '20-01-2004', '14-04-2004', '14-07-2004', '07-10-2004',
    '18-01-2005', '13-04-2005', '13-07-2005', '11-10-2005',
    '18-01-2006', '12-04-2006', '20-07-2006', '18-10-2006',
    '23-01-2007', '19-04-2007', '19-07-2007', '18-10-2007',
    '17-01-2008', '17-04-2008', '17-07-2008', '16-10-2008',
    '22-01-2009', '21-04-2009', '21-07-2009', '15-10-2009',
    '21-01-2010', '15-04-2010', '15-07-2010', '14-10-2010',
    '20-01-2011', '21-04-2011', '21-07-2011', '27-10-2011',
    '24-01-2012', '19-04-2012', '19-07-2012', '18-10-2012',
    '22-01-2013', '18-04-2013', '18-07-2013', '17-10-2013',
    '21-01-2014', '17-04-2014', '17-07-2014', '16-10-2014',
    '20-01-2015', '15-04-2015', '16-07-2015', '15-10-2015',
    '19-01-2016', '21-04-2016', '21-07-2016', '20-10-2016',
    '31-01-2017', '01-05-2017', '25-07-2017', '24-10-2017',
    '30-01-2018', '25-04-2018', '25-07-2018', '24-10-2018',
    '29-01-2019', '30-04-2019', '30-07-2019', '29-10-2019',
    '28-01-2020', '28-04-2020', '28-07-2020', '27-10-2020',
    '26-01-2021', '27-04-2021', '27-07-2021', '26-10-2021',
    '01-02-2022', '03-05-2022', '02-08-2022', '01-11-2022',
    '31-01-2023', '02-05-2023', '01-08-2023', '31-10-2023',
    '30-01-2024', '30-04-2024', '30-07-2024'
]

# Folder to save individual files
output_folder = 'quarterly_data'
os.makedirs(output_folder, exist_ok=True)

# Combine all data
combined_data = pd.DataFrame()

for date_str in earnings_dates:
    earning_date = datetime.strptime(date_str, '%d-%m-%Y')
    try:
        last_30_days_data = extract_30_data_points(data, earning_date)
        # Save individual file as CSV
        output_file_path = os.path.join(output_folder, f'last_30_days_{date_str}.csv')
        last_30_days_data.to_csv(output_file_path, index=False)
        
        # Append to combined data
        combined_data = pd.concat([combined_data, last_30_days_data], ignore_index=True)
    except ValueError as e:
        print(f"Skipping {date_str}: {e}")

# Save combined data as CSV
combined_output_path = 'combined_30_days_data.csv'
combined_data.to_csv(combined_output_path, index=False)

print(f"All data combined and saved to {combined_output_path}")
