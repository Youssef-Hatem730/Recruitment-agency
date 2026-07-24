# Deterministic Router

## How to Run

1. Install the required packages:

```bash
pip install google-genai python-dotenv PyPDF2 python-docx ddgs
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

5. Choose one of the available options:

- **Search for a Job**
- **Match My CV**
- **Exit**

This implementation is a **Deterministic Router**. The Gemini model is constrained to select exactly one job from the predefined `jobs.json` database. The application validates the returned job title before displaying the job details, ensuring deterministic routing without generating unsupported job categories.