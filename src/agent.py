from langchain.llms import OpenAI
import pandas as pd
import os
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.agents.agent import AgentExecutor
from langchain.chains.llm import LLMChain
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.prompts.prompt import PromptTemplate
from prompt import DEFAULT_PREFIX, DEFAULT_SUFFIX, DEFAULT_INPUT_VARIABLES



def _create_tools(locals: dict) -> list[PythonAstREPLTool]:
    """Create the tools that the agent will use to answer questions.
    params:
        locals: Dictionary of objects to be passed to the Python REPL
    """
    return [PythonAstREPLTool(locals=locals)]

def _create_llm() -> OpenAI:
    """Create the language model that the agent will use to answer questions."""
    return OpenAI(temperature=0)

def _create_prompt(locals: dict,
                   tools: list[PythonAstREPLTool],
                   prefix :str = DEFAULT_PREFIX, 
                   suffix: str = DEFAULT_SUFFIX, 
                   input_variables: list[str] = DEFAULT_INPUT_VARIABLES) -> PromptTemplate:
    """Create the prompt that the agent will use to answer questions.
    params:
        locals: Dictionary of objects to be passed to the Python REPL
        tools: List of tools that the agent will use to answer questions
        prefix: The prefix of the prompt
        suffix: The suffix of the prompt
        input_variables: The variables to be injected into the prompt
    """
    prompt = ZeroShotAgent.create_prompt(
    tools, prefix=prefix, suffix=suffix, input_variables=input_variables)
    partial_prompt = prompt.partial()
    partial_prompt = partial_prompt.partial(
    df_head=str(locals['df'].head(5).to_markdown()),
    plotting_function_code=locals['plotting_function_code'],
    chart_context=locals['chart_context']
    )
    return partial_prompt


def _create_llm_chain(locals, tools, callback_manager = None) -> LLMChain:
    """Create the LLMChain that the agent will use to answer questions."""
    return LLMChain(
            llm=_create_llm(),
            prompt=_create_prompt(locals, tools),
            callback_manager=callback_manager,
        )

def _create_agent(locals, tools, callback_manager=None) -> ZeroShotAgent:
    """Create the agent that will answer questions."""
    return ZeroShotAgent(
            llm_chain=_create_llm_chain(locals, tools),
            allowed_tools=[tool.name for tool in tools],
            callback_manager=callback_manager,
        )

def create_custom_pandas_agent_executor(locals: dict, callback_manager = None) -> AgentExecutor:
    """Create the AgentExecutor that will answer questions."""
    tools = _create_tools(locals)
    return AgentExecutor.from_agent_and_tools(
            agent=_create_agent(locals, tools),
            tools=tools,
            callback_manager=callback_manager,
            verbose=True,
            return_intermediate_steps=False,
            max_iterations=15,
            max_execution_time=None,
            early_stopping_method="force",
        )