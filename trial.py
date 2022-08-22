# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import date
import yfinance as yf

'''
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

item1 = html.Div(
    [
        html.P("Welcome to the Stock Dash App!", className="start"),
        html.Div([
            # stock code input
            html.P("Input stock code: "),
            dcc.Input(
                id="stock-input",
                type="text",
                placeholder=""
            ),
            html.Button('Submit', id='submit-val')
            
        ]),
        #Date range picker input
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2017, 9, 19),
                initial_visible_month=date(2017, 8, 5),
                end_date=date(2017, 8, 25)
            )
            
        ]),
        html.Div([
            #stock price button
            html.Button('Stock Price', id='stock-price'),
            #indicators button
            html.Button('Indicators', id='indicators'),
            #number of days of forecast input
            dcc.Input(
                id="input",
                type="number",
                placeholder="number of days"
            ),
            #forecast button
            html.Button('Forecast', id='forecast'),
        ]),
    ],
    className="nav")

item2 = html.Div(
    [
            html.Div(
                  [  # Logo
                    # Company Name
                  ],
                className="header"),
            html.Div( #Description
              id="description", className="decription_ticker"),
            html.Div([
                # Stock price plot
            ], id="graphs-content"),
            html.Div([
                # Indicator plot
            ], id="main-content"),
            html.Div([
                # Forecast plot
            ], id="forecast-content")
          ],
          className="content")


app.layout = html.Div([item1, item2])



if __name__ == '__main__':
    app.run_server(debug=True)
    
'''
def get_stock_price_fig(df):
    fig = px.line(df,
                  x="Date",
                  y=["Open", "Close"],
                  title="Closing and Opening Price vs Date")
    fig.show()
    return fig 

def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                    x="Date",
                    y="EWA_20",
                    title="Exponential Moving Average vs Date")

    fig.update_traces(mode="markers")
    fig.show() 
    return fig

ticker = yf.Ticker('AAPL')
inf = ticker.info
df = pd.DataFrame().from_dict(inf, orient="index").T
print(df['shortName'][0])
#print(inf['longBusinessSummary'])
old  =  yf.download("AAPL", start="2010-01-01",  end="2020-07-21")
old = old.reset_index()
for i in ['Open', 'High', 'Close', 'Low']: 
      old[i]  =  old[i].astype('float64')
import plotly.express as px
#fig = px.line(old, x="Date", y=["Open", "Close"], title='PFizer Stock Prices')
#fig.show()
#data = yf.download("AMZN", start="2017-01-01", end="2017-04-30")
#get_stock_price_fig(data)
#old['EWA_20'] = old['Close'].ewm(span=20, adjust=False).mean()
get_stock_price_fig(old)
