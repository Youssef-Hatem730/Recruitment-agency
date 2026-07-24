from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_core.utils.json import parse_json_markdown

load_dotenv()

LLM= ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

system_prompt=("you are a job recruiter agent search for the given job, search for avilable jobs in known recruiters sites ")

memory=MemorySaver()


agent=create_agent(
    model=LLM,
    checkpointer=memory,
    system_prompt=system_prompt,
)
config = {"configurable": {"thread_id": "user_session_abc123"}}

while(True):
    print("Welcome to job agency app (q to exit)")
    user_prompt=input(">")
    if(user_prompt=="q"):
        break
    response = agent.invoke({"messages": [("user", user_prompt)]}, config)
    
    raw=response["messages"][-1].content

    raw_text=raw[0].get("text","")
    full_data = parse_json_markdown(raw_text)
        
    results_only = full_data.get("Results", [])
    print(results_only)

