import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import linregress

# Load the data
df = pd.read_csv('aapl_us_d.csv')

# Print column names to understand the structure of the data
print("Column names in the dataset:")
print(df.columns)

# Map common column names to variables
date_col = [col for col in df.columns if 'date' in col.lower()][0]
open_col = [col for col in df.columns if 'open' in col.lower()][0]
high_col = [col for col in df.columns if 'high' in col.lower()][0]
low_col = [col for col in df.columns if 'low' in col.lower()][0]
close_col = [col for col in df.columns if 'close' in col.lower()][0]
volume_col = [col for col in df.columns if 'volume' in col.lower()][0]

# Convert the date column to datetime
df[date_col] = pd.to_datetime(df[date_col])

# Handle missing values if necessary
df.dropna(inplace=True)

# Basic Visualization: Plot Closing Prices
plt.figure(figsize=(12, 6))
plt.plot(df[date_col], df[close_col], label='Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Apple Stock Closing Prices Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Calculate Moving Averages
df['SMA_50'] = df[close_col].rolling(window=50).mean()
df['SMA_200'] = df[close_col].rolling(window=200).mean()

# Plot with Moving Averages
plt.figure(figsize=(12, 6))
plt.plot(df[date_col], df[close_col], label='Close Price')
plt.plot(df[date_col], df['SMA_50'], label='50-Day SMA', linestyle='--')
plt.plot(df[date_col], df['SMA_200'], label='200-Day SMA', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Apple Stock Closing Prices with Moving Averages')
plt.legend()
plt.grid(True)
plt.show()

# Fit a Linear Trendline
df['date_ordinal'] = df[date_col].map(pd.Timestamp.toordinal)
slope, intercept, r_value, p_value, std_err = linregress(df['date_ordinal'], df[close_col])

# Plot with Trendline
plt.figure(figsize=(12, 6))
plt.plot(df[date_col], df[close_col], label='Close Price')
plt.plot(df[date_col], intercept + slope * df['date_ordinal'], label='Trendline', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Apple Stock Closing Prices with Trendline')
plt.legend()
plt.grid(True)
plt.show()

# Interactive Plot with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], mode='lines', name='Close Price'))
fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_50'], mode='lines', name='50-Day SMA'))
fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_200'], mode='lines', name='200-Day SMA'))
fig.update_layout(title='Apple Stock Closing Prices with Moving Averages',
                  xaxis_title='Date',
                  yaxis_title='Price')
fig.show()

# Candlestick Chart with Plotly
fig = go.Figure(data=[go.Candlestick(x=df[date_col],
                                     open=df[open_col],
                                     high=df[high_col],
                                     low=df[low_col],
                                     close=df[close_col])])
fig.update_layout(title='Apple Stock Candlestick Chart',
                  xaxis_title='Date',
                  yaxis_title='Price')
fig.show()

# Volume Analysis
plt.figure(figsize=(12, 6))
plt.bar(df[date_col], df[volume_col], color='gray')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.title('Apple Stock Trading Volume')
plt.grid(True)
plt.show()

# Correlation Analysis
corr = df[[open_col, high_col, low_col, close_col, volume_col]].corr()
print("Correlation Matrix:")
print(corr)

