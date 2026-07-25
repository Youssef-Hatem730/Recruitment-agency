import os
import json
import fitz
from docx import Document
from tkinter import Tk, filedialog


# File Readers
def read_pdf(file_path):
    text = ""
    pdf = fitz.open(file_path)
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Read CV
def read_cv(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension == ".docx":
        return read_docx(file_path)

    elif extension == ".txt":
        return read_txt(file_path)

    else:
        raise ValueError("Unsupported file type")


# File Picker
def choose_cv():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(

        title="Select your CV",

        filetypes=[
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx"),
            ("Text files", "*.txt")
        ]
    )
    return file_path


# Load Jobs
def load_jobs(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        jobs = json.load(file)
    return jobs


# Search Job
def search_job():
    keyword = input("\nEnter Job Title: ").lower()

    jobs = load_jobs("jobs.json")

    found = False

    for job in jobs:

        if keyword in job["Title"].lower() or keyword in job["Description"].lower():

            found = True

            print("\n========== Matching Job ==========")
            print("Title       :", job["Title"])
            print("Description :", job["Description"])
            print("Location    :", job["Place"])
            print("Salary      :", job["Salary"])
            print("Apply Link  :", job["Apply_link"])
            print("==================================")

    if not found:

        print("\nNo matching jobs found.")


# HARD-CODED TECHNICAL KEYWORDS
TECH_KEYWORDS = [

    "python",
    "java",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",

    "django",
    "flask",
    "fastapi",
    "node.js",
    "express",

    "spring",
    "laravel",

    "tensorflow",
    "pytorch",
    "keras",

    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "git",
    "github",

    "linux",

    "excel",
    "power bi",
    "tableau"
]


# Extract Candidate Keywords
def extract_keywords(cv_text):
    cv_text = cv_text.lower()

    candidate_keywords = []

    for keyword in TECH_KEYWORDS:

        if keyword in cv_text:

            candidate_keywords.append(keyword)
    return candidate_keywords


MIN_MATCHES = 3

# Find Matching Job
def find_matching_job(candidate_keywords, jobs):

    for job in jobs:

        description = job.get("Description", "").lower()

        matched_keywords = []

        for keyword in candidate_keywords:

            if keyword in description:
                matched_keywords.append(keyword)

        if len(matched_keywords) >= MIN_MATCHES:
            return job, matched_keywords

    return None, []


# Build Output JSON
def build_output(selected_job):

    if selected_job is None:

        return {

            "job_title": "No suitable job found",
            "job_description": "",
            "job_salary": "",
            "url": ""
        }

    return {

        "job_title": selected_job.get("Title", ""),
        "job_description": selected_job.get("Description", ""),
        "job_salary": selected_job.get("Salary", ""),
        "url": selected_job.get("Apply_link", "")
    }


# Save Result
def save_result(result):
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

# Match CV
def match_cv():
    cv_path = choose_cv()

    if not cv_path:
        return
    
    try:
        cv_text = read_cv(cv_path)
    except Exception as e:

        print("\nError reading CV:")
        print(e)
        return

    candidate_keywords = extract_keywords(cv_text)

    print("\nCandidate Skills:")
    print(candidate_keywords)

    if len(candidate_keywords) == 0:

        result = {

            "job_title": "No suitable job found",
            "job_description": "",
            "job_salary": "",
            "url": ""
        }

        save_result(result)

        print("\nNo suitable job found.")
        return
    
    try:

        jobs = load_jobs("jobs.json")
    except Exception as e:

        print("\nError loading jobs.json")
        print(e)
        return

    selected_job, matched_keywords = find_matching_job(candidate_keywords, jobs)

    print("\nMatched Skills:")
    print(matched_keywords)

    result = build_output(selected_job)

    save_result(result)

    print("\n========== Recommended Job ==========\n")
    print("Title       :", result["job_title"])
    print("Description :", result["job_description"])
    print("Salary      :", result["job_salary"])
    print("URL         :", result["url"])

# Main
def main():

    while True:
        print("\n===================================")
        print("       Recruitment Agency")
        print("===================================")
        print("1. Search for a Job")
        print("2. Match My CV")
        print("3. Exit")

        choice = input("\nUser: ")

        if choice == "1" or choice.lower().find("jobs")!=-1:

            search_job()

        elif choice == "2" or choice.lower().find("cv")!=-1:

            match_cv()

        elif choice == "3":

            print("\nWishing you success in your career journey!")

            break

        else:

            print("\nInvalid choice. Try again.")


if __name__ == "__main__":
    main()
