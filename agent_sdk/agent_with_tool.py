from agents import Agent, FileSearchTool, Runner, WebSearchTool, function_tool
import asyncio
import requests
from dotenv import load_dotenv
load_dotenv()

@function_tool()
def get_weather(city: str):
    """ Fetch the weather for a given city name.
    Args:
        city: The city name to fetch the weather for 
     """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if(response.status_code == 200):
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        get_weather
    ],
)

async def main():
    result = await Runner.run(agent, "What is weather in goa right now?")
    print(result.final_output)

asyncio.run(main())