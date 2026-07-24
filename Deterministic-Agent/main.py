from dotenv import load_dotenv
import tools


load_dotenv()



# Deterministic Router
from google import genai
client = genai.Client()

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
            tools.search_job()
        elif choice == "2":
            tools.match_cv()
        elif choice == "3":
            print("\nWishing you success in your career journey!")
            break
        else:
            print("\nInvalid choice. Try again.")
if __name__ == "__main__":
    main()
