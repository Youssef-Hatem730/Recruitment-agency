!pip install PyPDF2 python-docx python-dotenv

from dotenv import load_dotenv
from google.colab import files
import io
import PyPDF2
import docx
import json
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Jobs
with open("jobs.json", "r", encoding="utf-8") as file:
    JOBS_DB = json.load(file)

# Search Job
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

# Extract text from file with extention(pdf,docx,txt)
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
        pdf = PyPDF2.PdfReader(io.BytesIO(content))
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    elif extension == "docx":
        document = docx.Document(io.BytesIO(content))
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    return text.lower()

# Match CV
def match_cv():

    print("\nUpload your CV (pdf / docx / txt)")
    uploaded = files.upload()
    if not uploaded:
        return

    filename = list(uploaded.keys())[0]
    cv_text = extract_text(filename, uploaded[filename])\
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

# Deterministic Router
from google import genai
client = genai.Client(api_key=api_key)

def main():
    while True:
        print("\n===================================")
        print("       Recruitment Agency")
        print("===================================")
        print("1. Search for a Job")
        print("2. Match My CV")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_job()
        elif choice == "2":
            match_cv()
        elif choice == "3":
            print("\nWishing you success in your career journey!")
            break
        else:
            print("\nInvalid choice. Try again.")
if __name__ == "__main__":
    main()
