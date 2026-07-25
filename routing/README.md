# Deterministic Router

## How to Run

1. Install the required packages:

```bash
pip install google-genai python-dotenv PyPDF2 python-docx
```

2. Create a `.env` file in the project folder and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

3. Place the following files in the same folder:

- `main.py`
- `jobs.json`
- `.env`

4. Run the program:

```bash
python main.py
```

5. Choose one of the available options:

- **Search for a Job** → Search for jobs by title or description from the local `jobs.json` database.
- **Match My CV** → Upload a CV (`.pdf`, `.docx`, or `.txt`). The system extracts the CV text and uses the Gemini model to deterministically route the candidate to exactly one job from the predefined job list.
- **Exit** → Close the application.

This implementation is a **Deterministic Router**. The Gemini model is constrained to choose exactly one job from the predefined `jobs.json` database. The returned job is validated against the available job list before displaying the recommendation and its details.