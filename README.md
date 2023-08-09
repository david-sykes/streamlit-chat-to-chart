# streamlit-chat-to-chart
A tool to allow you to easily turn a Streamlit chart into an AI data analyst helper. It uses a simple decorator pattern that can be wrapped around any function that generates a Streamlit chart to turn it into a chart you can chat with.

```
@chat_with_chart(df, output_dict={}, chart_context="Some useful extra context for your chart and data")
def your_plotting_function():
    plot_df = df.groupby(...).agg(...) ## Your data manipulation
    return st.write(px.bar(plot_df, x='...', y='...')) ## Your plotting logic
```

## Features
- Ask the AI helper anything about the chart or the underlying data
- The AI helper uses pandas to analyse and manipulate the data to answer your questions
- The AI helper is provided with the chart source code and context
- Downloadable csv outputs provided by the AI helper for follow up analysis 
- Built on top of the Langchain Pandas agent toolkit
- The Streamlit developer can add their own additional context with a simple decorator argument 

## Demo
[streamlit-app-2023-08-09-22-08-60.webm](https://github.com/david-sykes/streamlit-chat-to-chart/assets/18305148/5bac1837-dce7-473f-b3b6-4ec49d0a04e5)

## Example app
A simple example Streamlit app is provided to get started. 

To get this working:

1. Clone the repo locally
2. `cd` into the repo
3. Create a pipenv and install dependencies using `pipenv install` (or manually install using the requirements.txt)
4. Ensure you have a .env file containing `OPENAI_API_KEY=YOUR_OPENAI_KEY` in the project root directory
5. Move into the src directory `cd src/`
6. Start the app using `pipenv run streamlit run app.py`

## Useful references
- The Streamlit UI is adapted from Langchain's Streamlit chat to pandas df [here](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/chat_pandas_df.py)
- The example uses Kaggle's Top 2000 company dataset [here](https://www.kaggle.com/datasets/joebeachcapital/top-2000-companies-globally)
- The Agent is adapted from Langchain's Pandas agent toolkit [here](https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/agents/agent_toolkits/pandas)

## Warnings
NOTE (from the Langchain docs): this agent calls the Python agent under the hood, which executes LLM generated Python code - this can be bad if the LLM generated Python code is harmful. Use cautiously.
