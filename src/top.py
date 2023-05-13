import streamlit as st
from .utils import Make_grid, Markdown_html_text, Markdown_html_link, Img_html

def Top(data_obj):
    tickerData = data_obj.tickerData
    tickerSymbol = data_obj.symbol
    longname = tickerData.quote_type[tickerSymbol]['longName']
    Markdown_html_text(text = 'Finance Analysis Dashboard', align = 'center', level = 'h1')
    col1, col2 = st.columns([1,3])
    # Column 1
    summary_profile = tickerData.summary_profile[tickerSymbol]
    with col1:
        logo_path = r'logos/%s.png' % tickerSymbol
        Img_html(logo_path, align = 'center') 
        Markdown_html_text(text = tickerSymbol, align = 'center', level = 'h4')
        Markdown_html_link(text = longname,link = summary_profile['website'],align = 'center')
        st.markdown('`%s` `%s`' % ( summary_profile['sector'], summary_profile['industry']))


    # Column 2
    summary_detail = tickerData.summary_detail[tickerSymbol]
    financial_data = tickerData.financial_data[tickerSymbol]
    key_stats = tickerData.key_stats[tickerSymbol]
    technical_insights = tickerData.technical_insights[tickerSymbol]
    with col2:
        col21, col22 = st.columns([1,2])
        with col21:
            price_delta = round(financial_data["currentPrice"] - summary_detail['previousClose'],2)
            price_relative =  round((price_delta/ summary_detail['previousClose'])*100,2)
            st.metric(label="Price", value='%s %s ' % ( summary_detail['previousClose'], summary_detail['currency']), 
                    delta="{} {} ({}%)".format(price_delta, summary_detail['currency'],price_relative),
                    label_visibility = "collapsed")
        with col22:
            text = ' Highest price:  %s (%s) ' % ( round(summary_detail['dayHigh'],2), summary_detail['currency'])
            Markdown_html_text(text = text, align = 'left', level = 'p')
            text = 'Lowest price:  %s (%s) ' % ( round(summary_detail['dayLow'],2), summary_detail['currency'])
            Markdown_html_text(text = text, align = 'left', level = 'p')
        ratio_grid =  Make_grid(3,5)
        # Row 1st
        ratio_grid[0][0].markdown('Market Cap <br> **%sB %s**' % (round(summary_detail['marketCap']/1000000000,2), 'USD'), unsafe_allow_html=True)
        ratio_grid[0][1].markdown('Forward P/E <br> **%s**' % round(key_stats['forwardPE'],2), unsafe_allow_html=True)
        ratio_grid[0][2].markdown('Forward EPS <br> **%s**' % round(key_stats['forwardEps'],2), unsafe_allow_html=True)
        ratio_grid[0][3].markdown('Recommendation  <br> <font color="red"><b>**%s**</b></font>' % technical_insights['recommendation']['rating'], unsafe_allow_html=True)
        ratio_grid[0][4].markdown('Valuation <br> **%s**' % technical_insights['instrumentInfo']['valuation']['description'], unsafe_allow_html=True)
        # Row 2nd
        ratio_grid[1][0].markdown('Volume <br> **{:,}**'.format(summary_detail['volume']),unsafe_allow_html=True)
        ratio_grid[1][1].markdown('P/B <br> **%s**' % round(key_stats['priceToBook'],2), unsafe_allow_html=True)
        ratio_grid[1][2].markdown('Book value <br> **%s**' % round(key_stats['bookValue'],2), unsafe_allow_html=True)
        ratio_grid[1][3].markdown('Short-term <br> **%s**' % technical_insights['instrumentInfo']['technicalEvents']['shortTermOutlook']['indexDirection'], unsafe_allow_html=True)
        ratio_grid[1][4].markdown('Intermediate <br> **%s**' % technical_insights['instrumentInfo']['technicalEvents']['intermediateTermOutlook']['indexDirection'], unsafe_allow_html=True)
        # Row 3rd
        ratio_grid[2][0].markdown('Outstanding shares <br> **{:,}**'.format(key_stats['sharesOutstanding']), unsafe_allow_html=True)
        ratio_grid[2][1].markdown('EV/EBITDA <br> **%s**' % round(key_stats['enterpriseToEbitda'],2), unsafe_allow_html=True)
        ratio_grid[2][2].markdown('')
        ratio_grid[2][3].markdown('Long-term <br> **%s**' % technical_insights['instrumentInfo']['technicalEvents']['longTermOutlook']['indexDirection'], unsafe_allow_html=True)



    with st.expander("Company Business Summary",expanded = False):
            st.write(summary_profile['longBusinessSummary'])