from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import GraphRecursionError
from langchain.agents import create_agent
from pydantic import BaseModel,Field
import tools
from dotenv import load_dotenv

load_dotenv()

class Results(BaseModel):
    Title:str=Field(description="the job title")
    Description:str=Field(description="job Description")
    Place:str=Field(description="job place (country or state)")
    Salary:str=Field(description="job salary make it in US dollar with $ sign")
    Job_url:str=Field(description="the provided link for the job ")

class ResultsList(BaseModel):
    Results:list[Results]


LLM= ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

system_prompt=("you are a job recruiter agent look for jobs in known sites"
                "Your final response MUST fully populate the required structured JSON format dont include any other texts."
                )

memory=MemorySaver()

tool=[tools.match_cv,tools.Search_Jobs]

agent=create_agent(
    model=LLM,
    checkpointer=memory,
    tools=tool,
    system_prompt=system_prompt,
    response_format= ResultsList
)
config = {"configurable": {"thread_id": "user_session_abc123"},
        "recursion_limit": 3,
        "response_mime_type":"application/json",
        "response_schema":ResultsList
          }


while(True):
    print("Welcome to job agency app (q to exit)")
    user_prompt=input(">")
    if(user_prompt=="q"):
        break

    try:
        events = agent.stream(
                {"messages": [("user", user_prompt)]},
                stream_mode="values",config=config
            )
        
        for event in events:
            latest_message = event["messages"][-1]
                
            if latest_message.type == "ai":
                if latest_message.tool_calls:
                        print(f"[Tool Call]: {latest_message.tool_calls[0]['name']} with {latest_message.tool_calls[0]['args']}")
                else:
                        print(f"[Final Answer]:\n{latest_message.content}")
            elif latest_message.type == "tool":
                print(f"[Tool Output]: {latest_message.content}")
    except GraphRecursionError:
        print("done")

