import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px

# Streamlit page setup
st.set_page_config(page_title="Google Trends Dashboard", layout="wide")
st.title("📊 Google Trends Marketing Dashboard")
st.write("Enter a keyword below to see its real-time search trends on Google!")

# Input box for keyword
keyword = st.text_input("Enter a keyword (e.g. 'ChatGPT', 'Nike', 'Coca-Cola'):")

# Button to run the trend analysis
if st.button("Show Trends") and keyword:
    try:
        # Connect to Google Trends
        pytrends = TrendReq(hl='en-US', tz=360)

        # Build the search payload
        pytrends.build_payload([keyword], timeframe='today 3-m')

        # Fetch interest over time data
        data = pytrends.interest_over_time()

        if not data.empty:
            st.subheader(f"Search Interest for '{keyword}' (past 3 months)")
            
            # Line chart for search interest
            fig = px.line(data, x=data.index, y=keyword, title=f"Trend for '{keyword}'", markers=True)
            st.plotly_chart(fig)

            # Related queries (what else people search for)
            related_queries = pytrends.related_queries()
            top_queries = None
            if related_queries and keyword in related_queries:
                top_queries = related_queries[keyword].get('top')
            
            if top_queries is not None and not top_queries.empty:
                st.subheader("🔥 Top Related Queries")
                st.dataframe(top_queries.head(10))
            else:
                st.info("No related queries available for this keyword.")
        else:
            st.warning("No data found. Try another keyword or check spelling.")

    except Exception as e:
        st.error(f"Error: {e}")
