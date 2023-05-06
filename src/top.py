import streamlit as st
from .utils import Make_grid

def Top(data_obj):
    tickerData = data_obj.tickerData
    tickerSymbol = data_obj.symbol
    longname = tickerData.quote_type[tickerSymbol]['longName']
    st.markdown('<h1 style="text-align: center;">Finance Analysis Dashboard</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([1,2.5])
    # Column 1
    summary_profile = tickerData.summary_profile[tickerSymbol]
    with col1:
        st.markdown('**{}**'.format(tickerSymbol))
        st.markdown(longname)
        st.markdown(' `%s` `%s` ' % ( summary_profile['sector'], summary_profile['industry']))
        st.markdown('*[Website]({})*'.format(summary_profile['website']))


    # Column 2
    summary_detail = tickerData.summary_detail[tickerSymbol]
    financial_data = tickerData.financial_data[tickerSymbol]
    key_stats = tickerData.key_stats[tickerSymbol]
    with col2:
        col21, col22 = st.columns(2)
        with col21:
            price_delta = round(financial_data["currentPrice"] - summary_detail['previousClose'],2)
            price_relative =  round((price_delta/ summary_detail['previousClose'])*100,2)
            # st.markdown('Current price')
            st.metric(label="Price", value='%s %s ' % ( summary_detail['previousClose'], summary_detail['currency']), 
                    delta="{} {} ({}%)".format(price_delta, summary_detail['currency'],price_relative),
                    label_visibility = "collapsed")
        with col22:
            st.markdown(' Highest price:  %s (%s) ' % ( round(summary_detail['dayHigh'],2), summary_detail['currency']))
            st.markdown(' Lowest price:  %s (%s) ' % ( round(summary_detail['dayLow'],2), summary_detail['currency']))
        ratio_grid =  Make_grid(3,3)
        ratio_grid[0][0].markdown('Market Cap <br> %s %s' % (round(summary_detail['marketCap']/1000000000,2), 'BUSD'), unsafe_allow_html=True)
        ratio_grid[0][1].markdown('Forward P/E <br> %s' % round(key_stats['forwardPE'],2), unsafe_allow_html=True)
        ratio_grid[0][2].markdown('Forward EPS <br> %s' % round(key_stats['forwardEps'],2), unsafe_allow_html=True)
        ratio_grid[1][0].markdown('Volume <br> %s' % round(summary_detail['volume'],2), unsafe_allow_html=True)
        ratio_grid[1][1].markdown('P/B <br> %s' % round(key_stats['priceToBook'],2), unsafe_allow_html=True)
        ratio_grid[1][2].markdown('Book value <br> %s' % round(key_stats['bookValue'],2), unsafe_allow_html=True)
        ratio_grid[2][0].markdown('Outstanding shares <br> %s' % round(key_stats['sharesOutstanding'],2), unsafe_allow_html=True)
        ratio_grid[2][1].markdown('EV/EBITDA <br> %s' % round(key_stats['enterpriseToEbitda'],2), unsafe_allow_html=True)
        ratio_grid[2][2].markdown('')



    with st.expander("Company Business Summary",expanded = False):
            st.write(summary_profile['longBusinessSummary'])

    # Get data and extract metrics
    financial_statement_df = data_obj.financial_statement_df
    # Ask for displaying raw data
    with st.container():
        show_data = st.checkbox("Do you want to see the full table of financial statement data?")
        if show_data:
            financial_statement_df