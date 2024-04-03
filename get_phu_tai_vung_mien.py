import requests
import pandas as pd
from datetime import datetime, timedelta

# Define start and end dates
start_date = pd.to_datetime("01/01/2024", format="%d/%m/%Y")
end_date = pd.to_datetime("02/04/2024", format="%d/%m/%Y")

# Generate daily dates between start and end date (inclusive)
date_range = pd.date_range(start_date, end_date, freq="D")

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame()

# Iterate over the date range, Fetch data from the API
for date in date_range:
    url = f"https://www.nldc.evn.vn/api/services/app/Pages/GetChartPhuTaiVM?day={date.strftime('%d/%m/%Y')}"
    response = requests.get(url)
    data_raw = response.json()
    # Convert to DataFrame
    phuTai = data_raw["result"]["data"]["phuTais"]
    # Convert to DataFrame and transpose
    df = pd.DataFrame(phuTai)
    # Set index starting from 1
    df.index = range(1, len(df) + 1)
    # Transpose the DataFrame
    df = df.transpose()
    # Extract hour and minute from "thoiGian" column
    df.loc[date.strftime('%d/%m/%Y')] = pd.to_datetime(df.loc["thoiGian"]).dt.strftime('%H:%M')
    # Drop the original "thoiGian" row
    df = df.drop("thoiGian")
    # Move the last row to the top
    df = pd.concat([df.iloc[-1:], df.iloc[:-1]])
    # Append the DataFrame to the result DataFrame
    result_df = pd.concat([result_df, df], ignore_index=False)

# Display the final result DataFrame
# print(result_df)

# Export DataFrame to Excel
result_df.to_excel("Phu_tai_VM_2024.xlsx")