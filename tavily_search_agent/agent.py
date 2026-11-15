from langchain_tavily import tavily_search
from google.adk.agents.llm_agent import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch

tavily_search = TavilySearch(
    max_result = 5,
    topic="general",
)

tavily_tool = LangchainTool(tool=tavily_search)


root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant that can search the web. ',
    instruction=(
        "Answer user questions accurately. "
        "Use the Tavily search tool when you need current information "
        "or need to verify facts"
        ),
    tools = [tavily_tool]
)
