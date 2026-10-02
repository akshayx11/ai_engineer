from dotenv import load_dotenv

from typing import List
from pydantic import BaseModel, Field
load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch

tavily = TavilyClient()

@tool
def search(query: str) -> str:
    """
    Tool that serach over internet
        Args:
            query: query to search for
        Returns:
            The search result
    """
    print("Searching for {query}")
    return tavily.search(query=query)
    # return "Tokyo weather is sunny"

@tool
def search_jobs(query: str) -> str:
    """
    Tool that serach over internet
        Args:
            query: query to search for
        Returns:
            The search result
    """
    print(f"Searching for jobs for query {query}")
    return tavily.search(query=query)
    # return "Tokyo weather is sunny"


class Source(BaseModel):
    """Schema for source used by agent"""

    url: str = Field(description="the url of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="The agent answers of the query")
    Source: List = Field(default_factory=list, description="List of sources to generate the answer")

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
# tools = [search]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Running agent")
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo?")})
    result = agent.invoke({"messages": HumanMessage(content="find the job opening for python developer in Bengaluru area for 7 years of experience candidate on LinkedIn")})

    print(result)

main()