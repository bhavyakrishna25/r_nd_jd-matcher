# AI Resume Matcher Frontend

This is a simple one-page Angular frontend for the Resume vs Job Description Matcher project.

## What the Frontend Does

- Upload a resume
- Paste a job description
- Click `Analyze`
- Show:
  - match percentage
  - matched skills
  - missing skills
  - suggestions

## UI Structure

```text
App
|-- Upload Section
|-- Job Description Input
|-- Analyze Button
`-- Result Section
```

## Components

- `upload-resume`
- `job-description`
- `analyze-button`
- `results`

## Shared State

The app uses one shared service:

- `AnalysisService`

It stores:

- selected resume file
- job description text
- API response
- loading state
- error message

## Setup

1. Install Angular CLI if needed:

```bash
npm install -g @angular/cli
```

2. Install project dependencies:

```bash
cd frontend
npm install
```

3. Run the Angular app:

```bash
ng serve
```

4. Open in your browser:

```text
http://localhost:4200
```

## Backend Requirement

Run the FastAPI backend on:

```text
http://127.0.0.1:8000
```

The frontend sends a `POST` request to:

```text
/analyze
```

with:

- `resume` as file
- `job_description` as form text

## Build Order Used

1. UI inputs
2. Shared service for state
3. Analyze button logic
4. API call with `HttpClient`
5. Result rendering
6. Styling, loading state, and error handling
