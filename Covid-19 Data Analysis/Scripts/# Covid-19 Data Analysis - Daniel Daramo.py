# Covid-19 Data Analysis, Daniel Daramola
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests

print("All libraries imported successfully!")

# Loading Datasets
cases = pd.read_csv(r"C:\Users\danie\OneDrive - UNT System\Desktop\Projects\Covid-19 Data Analysis\worldometer_coronavirus_daily_data.csv")
world_summary = pd.read_csv(r"C:\Users\danie\OneDrive - UNT System\Desktop\Projects\Covid-19 Data Analysis\worldometer_coronavirus_summary_data.csv")

# Previewing Datasets
print(cases.head())
print(world_summary.head())

# Inspecting and Cleaning Data
print(cases.info())
print(world_summary.info())

# Checking for missing values
missing_values = cases.isnull().sum()
if missing_values.any():
    print("Missing values found in columns:")
    print(missing_values[missing_values > 0])

# Dropping missing values
cases.dropna(inplace=True)

# Filling missing values in data with 0
cases.fillna(0, inplace=True)
world_summary.fillna(0, inplace=True)

# Aggregating daily data
cases['date'] = pd.to_datetime(cases['date'])
daily_cases = cases.groupby("date")["daily_new_cases"].sum()

# Smoothing data with 7-day rolling average
daily_cases_smoothed = daily_cases.rolling(window=7).mean()

# Plotting a graph
plt.figure(figsize=(10, 6))
plt.plot(daily_cases_smoothed, label='New Cases (7-Day Avg)')
plt.title('Global Daily COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend()
plt.grid()
plt.show()

# Filtering top 5 affected countries
top_countries = world_summary.sort_values(by='total_cases_per_1m_population', ascending=False).head(10)
sns.barplot(x='country', y='total_cases_per_1m_population', data=top_countries)
plt.title('Top 10 Countries by Total Cases')
plt.xticks(rotation=45)
plt.show()

# Grouping daily cases by country and date
country_cases = cases.groupby(['country', 'date'])['daily_new_cases'].sum().reset_index()

# Select a specific country for analysis
country = 'USA'
country_data = country_cases[country_cases['country'] == country]

# Smoothing data with 7-day rolling average
country_data['new_cases_smoothed'] = country_data['daily_new_cases'].rolling(window=7).mean()

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(country_data['date'], country_data['new_cases_smoothed'], label=f'{country} (7-Day Avg)')
plt.title(f'COVID-19 Daily Cases in {country}')
plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend()
plt.grid()
plt.show()

# Calculating daily growth rate
growth_rate = daily_cases.pct_change().fillna(0) * 100

plt.figure(figsize=(10, 6))
plt.plot(growth_rate, label='Growth Rate (%)')
plt.title('Daily Growth Rate of COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('Growth Rate (%)')
plt.legend()
plt.grid()
plt.show()
