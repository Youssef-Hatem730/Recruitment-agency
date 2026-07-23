from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from pydantic import BaseModel,Field
from dotenv import load_dotenv
import json
from langchain_core.utils.json import parse_json_markdown

load_dotenv()

class Results(BaseModel):
    Title:str=Field(description="the job title")
    Description:str=Field(description="job Description")
    Place:str=Field(description="job place (country or state)")
    Salary:str=Field(description="job salary make it in US dollar with $ sign")
    Apply_link:str=Field(description="the provided apply link for the job ")

class ResultsList(BaseModel):
    Results:list[Results]


LLM= ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

system_prompt=("you are a job recruiter agent search for at least 5 given user jobs, search for avilable jobs in known recruiters sites "
                "Your final response MUST fully populate the required structured JSON format dont include any other texts."
                "Remeber recent history chat it will be given as 'assistant role' "
                )
memory=MemorySaver()


agent=create_agent(
    model=LLM,
    checkpointer=memory,
    system_prompt=system_prompt,
    response_format= ResultsList
)
config = {"configurable": {"thread_id": "user_session_abc123"}}
while(True):
    print("Welcome to job search app (q to exit)")
    user_prompt=input(">")
    if(user_prompt=="q"):
        break
    response = agent.invoke({"messages": [("user", user_prompt)]}, config)
    
    raw=response["messages"][-1].content

    raw_text=raw[0].get("text","")
    full_data = parse_json_markdown(raw_text)
        
    results_only = full_data.get("Results", [])
    print(results_only)

