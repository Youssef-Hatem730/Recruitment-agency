# Constraint_React

## How to Run

1. Install the required packages:

```bash
pip install langchain langchain-community python-dotenv pydantic langchain-google-genai langgraph
```

2. Create a `.env` file in the project folder and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

3. Place the following files in the same folder:

- `main.py`
- `tools.py`
- `jobs.json`
- `.env`

4. Run the program:

```bash
python main.py
```

5. The Agent will wait for user input:
- **If the user typed something related to job search it will excute the job search tool**

- **If the user Wants to check on cv the agent will excute the match cv tool**

- **The agent will remember old chat history**

-**the output will be in formated json**


- **q** → Close the application.