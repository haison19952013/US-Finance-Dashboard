import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def Make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def Price_plot(symbol, tickerData, start_date = '2022-01-01',end_date = '2022-05-05', interval = '1d'):
    price_data = tickerData.history(start=start_date, end=end_date, period='ytd', interval= interval)
    price_data = price_data.reset_index()

    # Create the candlestick chart using plotly
    fig = go.Figure(data=[go.Candlestick(x=price_data.date,
                                        open=price_data['open'],
                                        high=price_data['high'],
                                        low=price_data['low'],
                                        close=price_data['close'])])

    fig.update_layout(
        title={
            'text': f"{symbol} Stock Price ({start_date} - {end_date})",
            'font': {'family': "Arial", 'size': 18, 'color': "#7f7f7f"},
            'x': 0.25, # Set to 0.5 for center position or to a value >0.5 for right alignment
            'y': 0.9, # Set to 1.0 for top alignment or to a smaller value for lower position
        },
        xaxis_title="Date",
        yaxis_title="Price ($)",
    )
    return fig

def Time_series_plot(financial_statement_df,x,y,xlabel,ylabel,kind = 'line'):
    df = financial_statement_df
    # Plot data
    (fig, ax) = plt.subplots(1, 1, figsize=(6, 4))
    # Create a plot
    df.plot(x = x, y = y, kind = kind,ax = ax,legend = None)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(labelsize=12, labelrotation = 0)
    ax.grid(True)
    return fig

def Gauge_plot(financial_statement_df,y,ylabel,ref_value = 1.0):
    # gauge chart using plotly
    df = financial_statement_df
    # Filter data to take the latest year
    df = df[df['asOfDate'] == df['asOfDate'].max()]
    fig = go.Figure(go.Indicator(delta = {'reference': ref_value},
        mode = "gauge+number+delta",
        value = df[[y]].values.tolist()[0][0],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': ylabel}))
    fig.update_layout(font=dict(size=20))
    return fig

def Bullet_plot(financial_statement_df, y, ylabel, ref_value=1.0, min=-4, max=8):
    # bullet chart using plotly
    df = financial_statement_df
    # Filter data to take the latest year
    df = df[df['asOfDate'] == df['asOfDate'].max()]
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta", value=df[[y]].values.tolist()[0][0],
        domain={'x': [0.25, 1], 'y': [0, 1]},
        title={'text': "<b>%s</b>" % ylabel, 'align': "center"},
        delta={'reference': ref_value},
        gauge={
            'shape': "bullet",
            'axis': {
                'range': [min, max],
                'tickmode': 'linear',
                'dtick': 2.0
            },
            'threshold': {
                'line': {'color': "black", 'width': 3.5},
                'thickness': 1.,
                'value': df[[y]].values.tolist()[0][0]
            },
            'steps': [{'range': [min, ref_value-1], 'color': 'lightgray'},
                {'range': [ref_value-1, ref_value+1], 'color': 'gray'},
                {'range': [ref_value+1, max], 'color': 'lightgray'}],
            'bar': {'color': "black", 'thickness': 0}
        }
    ))

    fig.update_layout(height=250, font=dict(size=20))
    return fig