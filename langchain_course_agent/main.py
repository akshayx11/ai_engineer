from dotenv import load_dotenv

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

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
# tools = [search]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)


def main():
    print("Running agent")
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo?")})
    result = agent.invoke({"messages": HumanMessage(content="find the job opening for python developer in Bengaluru area for 7 years of experience candidate on LinkedIn")})

    print(result)

main()