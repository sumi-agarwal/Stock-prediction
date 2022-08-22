from cgitb import html
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def get_stock_price_fig(df):
    for i in ['Open', 'High', 'Close', 'Low']: 
      df[i]  =  df[i].astype('float64')
    fig = px.line(df,
                  x= "Date",
                  y= ["Open", "Close"],
                  title="Closing and Opening Price vs Date")
    return fig

def get_more(df):
    df["EWA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                    x= "Date",
                    y= "EWA_20",
                    title="Exponential Moving Average vs Date")

    fig.update_traces(mode="markers")
    
    return fig

app = dash.Dash(__name__)
server = app.server

item1 = html.Div(
    [
        html.P("Welcome to the Stock Dash App!", className="start"),
        html.Div([
            # stock code input
            html.P("Input stock code: "),
            dcc.Input(
                id="stock-input",
                type="text",
                placeholder="AAPL",
            ),
            html.Button('Submit', id='submit-val')
            
        ]),
        #Date range picker input
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=date.today(),
                end_date=date.today()
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
                  html.Img(id="logo"),
                  # Company Name
                  html.H1(id = "name")
                  ],
                className="header"),
            html.Div( #Description
              id="description", className="decription_ticker"),
            html.Div([
                dcc.Graph(id="graphs-content")
                # Stock price plot
            ]),
            html.Div([
                dcc.Graph(id="main-content")
                # Indicator plot
            ]),
            html.Div([
                # Forecast plot
            ], id="forecast-content")
          ],
          className="content")


app.layout = html.Div([item1, item2], className="container")

@app.callback([
    Output("logo", "src"),
    Output("name", "children"),
    Output("description", "children")
    ],
  #[d.Input("submit-val", "value")],
  [Input("stock-input", "value")]
  )
def update_data(val):  # input parameter(s)
    ticker = yf.Ticker(val)
    inf = ticker.info
    df = pd.DataFrame().from_dict(inf, orient="index").T
    name = df['shortName'][0]
    logo = df['logo_url'][0]
    description = df['longBusinessSummary'][0]
    return logo, name, description

@app.callback(
   Output("graphs-content", "figure"),
   [
    Input("stock-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    #Input("stock-price", "value")
])
def update_stock(val, start_date, end_date):
    df = yf.download(val, start_date, end_date)
    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return fig

@app.callback(
   Output("main-content", "figure"),
   [
    Input("stock-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    #Input("stock-price", "value")
])
def update_indicator(val, start_date, end_date):
    df = yf.download(val, start_date, end_date)
    df.reset_index(inplace=True)
    fig = get_more(df)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)