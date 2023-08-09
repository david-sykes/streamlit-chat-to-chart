# streamlit-chat-to-chart
A tool to allow you to easily turn a Streamlit chart into an AI data analyst agent.

## Features
- Simple decorator pattern, can be wrapped around any Streamlit element to turn it into a chattable chart
- Ask the AI agent anything about the chart or the underlying data
- AI agent is provided with the chart source code and context
- The Streamlit developer can add their own additional context with a simple decorator argument 
- Downloadable csv output from the Chart AI agent for follow up analysis 
- Built on top of Langchain AgentExecutor




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
