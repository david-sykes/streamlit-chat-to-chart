import streamlit as st
import pandas as pd
from plotly import express as px
from chart_decorator import chat_with_chart

## Read in the data
df = pd.read_csv('Top2000CompaniesGlobally.csv')


## Define a function that writes a streamlit plot. This function should contain the code that creates the dataframe to plot
# from the raw data and the code that creates the plot itself. This is because the agent will use the code to understand the 
# context of the plot. You should also feed it the raw dataframe and some additional context.
@chat_with_chart(df, output_dict={}, chart_context="A chart of the total market value by Country for the top 2000 global companies.")
def create_market_cap_plot():
    plot_df = df.groupby('Country').agg({'Market Value ($billion)': 'sum'}).reset_index().sort_values('Market Value ($billion)', ascending=False).head(30)
    return st.write(px.bar(plot_df, x='Country', y='Market Value ($billion)'))


st.title("Top 30 countries by market cap")

create_market_cap_plot()