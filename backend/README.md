# AI Resume Matcher Backend

This backend powers the AI-Based Resume vs Job Description Matcher project.

We are building it in small phases so the code stays modular, easy to understand, and easy to extend.

## Development Phases

1. Resume parsing
2. Text preprocessing
3. Skill extraction
4. Matching algorithm
5. API development
6. Frontend integration

## Phase 1 Goal

Extract clean text from uploaded resumes in:

- PDF format
- DOCX format

## Project Structure

```text
backend/
|-- app/
|   |-- main.py
|   |-- parsers/
|   |   `-- resume_parser.py
|   `-- utils/
|       `-- text_cleaner.py
`-- requirements.txt
```

## How Phase 1 Works

1. The user uploads a resume.
2. The API validates the file type.
3. The parser extracts text from the PDF or DOCX file.
4. The cleaner normalizes spaces and line breaks.
5. The API returns both raw and cleaned text.

## Required Libraries

- `fastapi`: create the API
- `uvicorn`: run the FastAPI server
- `python-multipart`: handle file uploads
- `PyPDF2`: extract text from PDF files
- `python-docx`: extract text from DOCX files

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

## Test Endpoint

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

- `GET /`
- `POST /extract-text`
- `POST /analyze`

## Phase 1 Output

The `/extract-text` endpoint returns:

- `filename`
- `raw_text`
- `cleaned_text`
- `character_count`

Example response:

```json
{
  "filename": "resume.pdf",
  "raw_text": "Original extracted text...",
  "cleaned_text": "Cleaned extracted text...",
  "character_count": 1240
}
```

## Analyze Endpoint

The `/analyze` endpoint accepts:

- `resume` as a file upload
- `job_description` as form text

It returns:

```json
{
  "match_percentage": 72.73,
  "tfidf_similarity": 68.41,
  "matched_skills": ["python", "sql"],
  "missing_skills": ["aws", "docker"],
  "suggestions": [
    "Add Aws experience to your resume.",
    "Learn Aws to improve your match."
  ]
}
```

## TF-IDF Phase

The backend now uses two comparison methods:

- `match_percentage`: keyword skill overlap
- `tfidf_similarity`: text similarity between the resume and job description

This keeps the original beginner-friendly skill match while adding a stronger NLP-based signal.
