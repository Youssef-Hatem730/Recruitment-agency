import dotenv
from langchain_core.tools import tool
from google import genai
from ddgs import DDGS
from tkinter import filedialog
import io
import PyPDF2
import os  
import docx
import json


dotenv.load_dotenv()
client = genai.Client()
with open("Constrained-React\\jobs.json", "r", encoding="utf-8") as file:
    JOBS_DB = json.load(file)

def extract_text(filename, content):

    extension = filename.split(".")[-1].lower()

    if extension not in ["pdf", "docx", "txt"]:
        print("\n Unsupported file format.")
        print("Please upload only PDF, DOCX, or TXT files.")
        return None

    text = ""

    if extension == "txt":
        text = content.decode("utf-8")

    elif extension == "pdf":
        pdf = PyPDF2.PdfReader(content)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    elif extension == "docx":
        document = docx.Document(io.BytesIO(content))
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    return text.lower()

def match_cv():


    """Check and rate the cv and recommend what to improve"""
    print("\nUpload your CV (pdf / docx / txt)")

    file_path = filedialog.askopenfilename(
    title="Select a File")
      

    filename=os.path.basename(file_path)
    cv_text = extract_text(filename, file_path)

    if cv_text is None:
        return

    if not cv_text.strip():
        print("Could not extract text from the uploaded file.")
        return

    jobs = [job["Title"] for job in JOBS_DB]

    prompt = f"""
    You are a deterministic routing agent for a recruitment company.

    Your task is to classify the candidate into ONE AND ONLY ONE job.

    Available jobs:

    {chr(10).join(jobs)}

    Rules:

    1. Choose exactly ONE job from the list above.
    2. Never invent a new job title.
    3. Do not recommend multiple jobs.
    4. Return ONLY valid JSON.
    5. Do not use markdown.

    Format:

    {{
        "job":"Backend Developer",
        "reason":"Python, Django, SQL"
    }}

    Candidate CV:

    {cv_text}
    """
    
    response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    response_text = response.text.strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:

        result = json.loads(response_text)

        selected_job = result["job"]

        if selected_job in jobs:

            print("\n========== Recommended Job ==========\n")

            print("Job    :", selected_job)
            print("Reason :", result["reason"])
            print()

            for job in JOBS_DB:

                if job["Title"] == selected_job:

                    print("Description :", job["Description"])
                    print("Location    :", job["Place"])
                    print("Salary      :", job["Salary"])
                    print("Apply Link  :", job["Apply_link"])
                    break

        else:

            print("The model returned an unsupported job.")

    except Exception as e:
        print("Error:", e)

    return response_text

def Search_Jobs(query: str) -> str:
    """Searches for avaialbe jobs ."""
    results = []
    with DDGS() as Search:
        for r in Search.text(query, max_results=10):
            results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}")

    return "\n---\n".join(results)
   

def search_job():
    keyword = input("\nEnter Job Title: ").lower()
    found = False

    for job in JOBS_DB:
        if keyword in job["Title"].lower() or keyword in job["Description"].lower():
            found = True
            print("\n========== Matching Job==========")
            print("Title       :", job["Title"])
            print("Description :", job["Description"])
            print("Location    :", job["Place"])
            print("Salary      :", job["Salary"])
            print("Apply Link  :", job["Apply_link"])
            print("===============================\n")

    if not found:
        print("\nNo matching jobs found.\n")
