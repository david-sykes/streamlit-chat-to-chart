import streamlit as st
import pandas as pd
from agent import create_custom_pandas_agent_executor
from langchain.callbacks import StreamlitCallbackHandler
import inspect



def convert_df(df):
    """Helper function to convert a pandas dataframe to a string."""
    return df.to_csv(index=False).encode('utf-8')



def chat_with_chart(df_for_agent: pd.DataFrame,
                   output_dict: dict,
                   chart_context: str = "This is a chart"):
    """Wrapper around decorator - so it can take arguments."""
    # This is the actual decorator function
    def decorator_function(plotting_function):
        # This is the wrapper function that modifies/extends the behavior of target_function
        def wrapper_function(*args, **kwargs):
            ## Plotting function is called first to render the actual plot
            plotting_function()
            
            ## Plotting function source code is extracted and passed to the agent for context
            plotting_function_code = inspect.getsource(plotting_function)

            ## Create the agent
            locals = {'df': df_for_agent, 'output_dict': output_dict, 'plotting_function_code': plotting_function_code, "chart_context": chart_context}
            pandas_df_agent = create_custom_pandas_agent_executor(locals=locals)
            
            ## Create the chat interface - code is adapted from https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/chat_pandas_df.py
            if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
                st.session_state["messages"] = [{"role": "assistant", 
                                                 "content": "Do you have any questions about this chart?"}]

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input(placeholder="What is this data about?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)

                with st.chat_message("assistant"):
                    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                    response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
                    if 'output_df' in output_dict:
                        try:
                            st.dataframe(output_dict['output_df'])
                            csv = convert_df(output_dict['output_df'])
                            st.download_button(
                            "Press to Download results",
                            csv,
                            "file.csv",
                            "text/csv",
                            key='download-csv')
                        except:
                            ##TODO  Need to handle the case where the output_df is not a dataframe
                            pass
            
        return wrapper_function

    return decorator_function
