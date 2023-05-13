import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64
from pathlib import Path

def Markdown_html_text(text,align = 'center',level = 'h1'):
    md_text = '<{} style="text-align: {};">{}</{}>'.format(level,align,text,level)
    st.markdown(md_text, unsafe_allow_html=True)

def Markdown_html_link(text,link,align = 'center'):
    md_text = '<div align="{}"><a href="{}">{} </a></div>'.format(align,link,text)
    st.markdown(md_text, unsafe_allow_html=True)

def Make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def Price_plot(tickerData, start_date = '2022-01-01',end_date = '2022-05-05', interval = '1d'):
    price_data = tickerData.history(start=start_date, end=end_date, period='ytd', interval= interval)
    price_data = price_data.reset_index()

    # Create the candlestick chart using plotly
    fig = go.Figure(data=[go.Candlestick(x=price_data.date,
                                        open=price_data['open'],
                                        high=price_data['high'],
                                        low=price_data['low'],
                                        close=price_data['close'])])
    fig.update_xaxes(title="X Axis Title", title_font=dict(size=18))
    fig.update_yaxes(title="Y Axis Title", title_font=dict(size=18))
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0},
        yaxis_title="Price (USD)",
        xaxis_title="",
        xaxis=dict(title_font=dict(size=20)),
        yaxis=dict(title_font=dict(size=20))
    )
    return fig

def Time_series_plot(df,x,y,xlabel,ylabel,kind = 'line'):
    plt.style.use('ggplot')
    # Plot data
    (fig, ax) = plt.subplots(1, 1, figsize=(6, 4))
    # Create a plot
    df.plot(x = x, y = y, kind = kind,ax = ax,legend = None, marker='o')
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(labelsize=12, labelrotation = 0)
    ax.grid(True)
    fig.set_tight_layout(True)
    return fig

def Gauge_plot(df,y,ylabel,ref_value = 1.0):
    # gauge chart using plotly
    # Filter data to take the latest year
    df = df[df['asOfDate'] == df['asOfDate'].max()]
    fig = go.Figure(go.Indicator(delta = {'reference': ref_value},
        mode = "gauge+number+delta",
        value = df[[y]].values.tolist()[0][0],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': ylabel}))
    fig.update_layout(font=dict(size=20))
    return fig

def Bullet_plot(df, y, ylabel, ref_value=1.0, min=-4, max=8):
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

def Create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV file</a>'
    return href

# Solution provided by dataprofessor (https://discuss.streamlit.io/t/image-in-markdown/13274/10) modified by mze3e to center the image
# img_to_bytes and img_to_html inspired from https://pmbaumgartner.github.io/streamlitopedia/sizing-and-images.html

def Img_html(img_path, align = 'center'):
    def img_to_bytes(img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes(img_path))
    st.markdown("<p style='text-align: {}; color: grey;'>".format(align) + img_html +"</p>", unsafe_allow_html=True)
    # return img_html