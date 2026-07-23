import os
import json
import fitz
from docx import Document


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


def load_jobs(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        jobs = json.load(file)
    return jobs


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

# EXTRACT CANDIDATE KEYWORDS
def extract_keywords(cv_text):
    cv_text = cv_text.lower()
    candidate_keywords = []
    for keyword in TECH_KEYWORDS:
        if keyword in cv_text:
            candidate_keywords.append(keyword)
    return candidate_keywords


MIN_MATCHES = 3

def find_matching_job(candidate_keywords, jobs):

    for job in jobs:
        description = job.get("Description", "").lower()
        matched_keywords = []

        #Comparimg candidate skills with job description
        for keyword in candidate_keywords:
            if keyword in description:
                matched_keywords.append(keyword)

        # Hard-coded condition
        if len(matched_keywords) >= MIN_MATCHES:
            print("Matched Skills:", matched_keywords)
            return job

    return None


# OUTPUT JSON
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


def save_result(result):

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)



def main():

    print("Reactive Recruitment Agent")
 
    cv_path = input("Enter CV file path: ")

    try:
        cv_text = read_cv(cv_path)
    except Exception as e:
        print("\nError reading CV:")
        print(e)
        return

    candidate_keywords = extract_keywords(cv_text)
    print("Candidate Skills:")
    print(candidate_keywords)

    if len(candidate_keywords) == 0:
        print("\nNo technical skills were found.")
        result = {
            "job_title": "No suitable job found",
            "job_description": "",
            "job_salary": "",
            "url": ""
        }
        save_result(result)
        return

    try:
        jobs = load_jobs("jobs.json")
    except Exception as e:
        print("\nError loading jobs.json")
        print(e)
        return


    selected_job = find_matching_job(candidate_keywords, jobs)
    result = build_output(selected_job)
    save_result(result)
    print("\nRecommended Job")
    print("-" * 20)

    print("Title :", result["job_title"])
    print("Description :", result["job_description"])
    print("Salary :", result["job_salary"])
    print("URL :", result["url"])


if __name__ == "__main__":
    main()