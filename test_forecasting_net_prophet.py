import re

def search_file(file, pattern):
    content = open(file).read()
    if re.search(pattern, content, re.MULTILINE | re.DOTALL):
        return True
    return False


### Find unusual patterns in hourly Google search traffic (25 points)
def test_traffic():
    assert search_file("forecasting_net_prophet.ipynb", rf"df_mercado_trends = pd\.read_csv\(.*\\\"https:\/\/static\.bc-edx\.com\/ai\/ail-v-1-0\/m8\/lms\/datasets\/google_hourly_search_trends\.csv\\\".*index_col=\'Date\',.*parse_dates=True,.*infer_datetime_format=True.*\)") == True, "Read the search data into a DataFrame. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"df_mercado_trends\[\\\"2020-05\\\"\]") == True, "Slice the data to just the month of May 2020. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"traffic_may_2020 = may_df\.sum\(\)") == True, "Calculate the total search traffic for the month.(5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"traffic_may_2020\/median_monthly_traffic") == True, "Compare the value to the monthly median across all months. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"Yes, but not much more than the overall trend \(see explaination above\)\.") == True, "Did the Google search traffic increase during the month that MercadoLibre released its financial results? Write your answer in the space provided in the starter file. (5 points)"

### Mine the search traffic data for seasonality (20 points)
def test_mine():
    assert search_file("forecasting_net_prophet.ipynb", rf"df_hour = df_mercado_trends\.groupby\(df_mercado_trends\.index\.hour\)\.mean\(\).*df_hour\.plot\(\)") == True, "Group the hourly search data to plot the average traffic by the hour of day. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"df_day = df_mercado_trends\.groupby\(df_mercado_trends\.index\.dayofweek\)\.mean\(\).*df_day\.plot\(\)") == True, "Group the hourly search data to plot the average traffic by the day of the week (for example, Monday vs. Friday). (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"df_week = df_mercado_trends\.groupby\(df_mercado_trends\.index\.isocalendar\(\)\.week\)\.mean\(\).*df_week\.plot\(\)") == True, "Group the hourly search data to plot the average traffic by the week of the year. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"There are clear trends in hour and day of week. Given that these times are likely in UTC, the peak hours look to be around 7 pm Eastern.*with the peak towards the beginning of the year, around week 4 and 9\.") == True, "Are there any time based trends that you can see in the data? Write your answer in the space provided in the starter file. (5 points)"

### Relate the search traffic to stock price patterns (35 points)'
def test_patterns():
    assert search_file("forecasting_net_prophet.ipynb", rf"df_mercado_stock = pd\.read_csv\(.*\\\"https:\/\/static\.bc-edx\.com\/ai\/ail-v-1-0\/m8\/lms\/datasets\/mercado_stock_price\.csv\\\",.*index_col=\\\"date\\\",.*parse_dates=True,.*infer_datetime_format=True.*\)\.dropna\(\).*df_mercado_stock\.plot\(\)") == True, "Read in and plot the stock price data. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"mercado_stock_trends_df = pd\.concat\(\[df_mercado_stock, df_mercado_trends\], axis=1\)\.dropna\(\)") == True, "Concatenate the stock price data to the search data in a single DataFrame. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"first_half_2020 = mercado_stock_trends_df\[\\\"2020-01\\\" : \\\"2020-06\\\"\]") == True, "Slice the data to just the first half of 2020 (2020-01 to 2020-06 in the DataFrame), and then plot the data. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"mercado_stock_trends_df\.assign\(\*\*\{{ \\\"Lagged Search Trends\\\": mercado_stock_trends_df\[\\\"Search Trends\\\"\]\.shift\(1\) \}}\)") == True, "Create a new column in the DataFrame named “Lagged Search Trends” that offsets, or shifts, the search traffic by one hour. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"mercado_stock_trends_df.assign\(\*\*\{{ \\\"Stock Volatility\\\": mercado_stock_trends_df\[\\\"close\\\"\]\.pct_change\(\)\.rolling\(window=4\)\.std\(\) \}}\)") == True, "Create two additional columns: “Stock Volatility”, which holds an exponentially weighted four-hour rolling average of the company’s stock volatility. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"mercado_stock_trends_df\.assign\(\*\*\{{ \\\"Hourly Stock Return\\\": mercado_stock_trends_df\[\\\"close\\\"\]\.pct_change\(\) \}}\)") == True, "Create two additional columns: “Hourly Stock Return”, which holds the percent change of the company's stock price on an hourly basis. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"The correlation between lagged search traffic and stock volatility is -0\.148938, and based on p-value is statistically significant.*sceptical to say the -0.15 correlation has much predictive power for stock volatility, and I definitely wouldn't conclude any sort of causation\.") == True, "Does a predictable relationship exist between the lagged search traffic and the stock volatility or between the lagged search traffic and the stock price returns? Write your answer in the space provided in the starter file. (5 points)"

### Create a time series model with Prophet (20 points)
def test_prophet():
    assert search_file("forecasting_net_prophet.ipynb", rf"prophet_df = df_mercado_trends\.reset_index\(\).*prophet_df\.columns = \[\\\"ds\\\", \\\"y\\\"\].*prophet_df\.dropna\(\)") == True, "Set up the Google search data for a Prophet forecasting model. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"forecast_mercado_trends = m\.predict\(future_mercado_trends\).*m\.plot\(forecast_mercado_trends\);") == True, "After estimating the model, plot the forecast. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"m\.plot_components\(forecast_mercado_trends\);") == True, "Plot the individual time series components of the model. (5 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"0, i.e., 12 am midnight\. If the times are in UTC, that would be 7 pm Eastern") == True, "What time of day exhibits the greatest popularity? (2 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"Tuesday") == True, "Which day of the week gets the most search traffic? (2 points)"

    assert search_file("forecasting_net_prophet.ipynb", rf"Around October 16th") == True, "What's the lowest point for search traffic in the calendar year? (1 point)"
