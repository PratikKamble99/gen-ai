import json
from openai import OpenAI
from dotenv import load_dotenv
import requests
from typing import Optional
from pydantic import BaseModel, Field

class OutputFormat(BaseModel):
    step: str = Field(..., description="The id of the step, Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional content for the step")
    tool: Optional[str] = Field(None, description="the ID of the tool to call")
    input: Optional[str] = Field(None, description="the inout params for the tool")

load_dotenv()

client = OpenAI()

# 1. Define a list of callable tools for the model if you are using client.response.create
# tools = [
#     {
#         "type": "function",
#         "name": "get_weather",
#         "description": "Get weather of provided city",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "city": {
#                     "type": "string",
#                     "description": "city of any country",
#                 },
#             },
#             "required": ["city"],
#         },
#     },
# ]

SYSTEM_PROMPT="""
    You are an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAn and OUTPUT steps.
    You need to first PLAN what need to be done, finally you can give OUTPUT.
    You call TOOL if required from list of available TOOLS.
    for every TOOl call wait for OBSERVER step Which is output from the called TOOL.

    Rules:
    - Strictly follow the give JSON output format.
    - Only run one step at time
    - The sequence of steps is START (Where user gives you input), PLAN (That can be multiple)

    OUTPUT JSON format:
    { "step":"START"|"PLAN"|"OUTPUT"|"TOOL"|"OBSERVER", "content":"string", "tool":"string", "input":"string"}

    AVAILABLE TOOLS:
    - get_weather(city:str): Takes city name as input string and returns the weather information.

    Example 1:
    START: {"step":"START", "input":"What is weather in goa?"}
    PLAN:  {"step":"PLAN", "content":"Seems like user interested in getting weather info"}
    PLAN:  {"step":"PLAN", "content":"Lets see if we have any available tools from list of available_tools"}
    PLAN:  {"step":"PLAN", "content":"I need to to call get_weather tool for delhi as input for city"}
    PLAN:  {"step":"TOOL", "tool":"get_weather", "input":"delhi"}
    PLAN:  {"step":"OBSERVE", "tool":"get_weather", "output":"The temperature of delhi is 20 C with some cloudy sky"}
    PLAN:  {"step":"PLAN", "content":"Got weather info from tool call"}
    OUTPUT: {"step":"OUTPUT", "content":"The current temperature of delhi is 20 C with some cloudy sky"}

    Example 2:
    START: {"step":"START", "input":"What is 2+2-2+1/2%2*21?"}
    PLAN:  {"step":"PLAN", "content":"Seems like user interested in Solving math problem"}
    PLAN:  {"step":"PLAN", "content":"I should solve this in step by step"}
    PLAN:  {"step":"PLAN", "content":"step-1 1/2"}
    OUTPUT: {"step":"OUTPUT", "content":"The result is"}
"""

input_list = [{"role": "system", "content": SYSTEM_PROMPT}]

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if(response.status_code == 200):
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools= {
    "get_weather": get_weather
}

def main():
    while True:
        user_query = input("> ")

        if user_query == "exit": break

        input_list.append({"role": "user", "content": user_query})
        
        while True:
            # response = client.chat.completions.create(
            #     model="gpt-5.2",
            #     messages=input_list,
            #     response_format={ "type": "json_object" },
            # )

            # IF YOU ARE USING Structured model outputs use .parse
            response = client.chat.completions.parse(
                model="gpt-5.2",
                messages=input_list,
                response_format=OutputFormat
            )

            # raw_result = response.choices[0].message.content
            # parsed_result = json.loads(raw_result)
            parsed_result = response.choices[0].message.parsed
            input_list.append({"role":"assistant", "content":json.dumps(parsed_result.model_dump())})


            # print(parsed_result)

            if parsed_result.step == "START":
                # print("🔥", parsed_result.get("content")) # Use if using normal json result
                print("🔥", parsed_result.content)
                continue

            if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                continue

            if parsed_result.step == "TOOL":
                tool = parsed_result.tool
                tool_input = parsed_result.input

                tool_response = available_tools[tool](tool_input)
                print(f"⚒️ {tool} - {tool_input} = {tool_response}")

                input_list.append({"role":"developer","content":json.dumps({
                    "step":"OBSERVE", "tool":tool, "input": tool_input, "output":tool_response
                })})

                continue

            if parsed_result.step == "OBSERVE":
                print("🤔", parsed_result.content)
                continue

            if parsed_result.step == "OUTPUT":
                print("🔚", parsed_result.content)
                break

            # continue
        #     for item in response.output:
        #         print(item)
        #         if item.type == "function_call":
        #             if item.name == "get_weather":
        #             print(item.arguments, "ARGUMENTS")
        #             weather = get_weather(json.loads(item.arguments)["city"])
                    
        #             input_list.append(item)
        #             input_list.append({
        #                 "type": "function_call_output",
        #                 "call_id": item.call_id,
        #                 "output": weather
        #             })

        #             print(response.output_text)

        #             print("Final input:")
        #             print(input_list)

        #             response = client.responses.create(
        #                 model="gpt-5.2",
        #                 input=input_list,
        #             )

        #             # 5. The model should be able to give a response!
        #             print("Final output:")
        #             print("\n" + response.output_text)
        # # If no tool was called
        # print(response.output_text)

main()
