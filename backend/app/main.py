from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.parsers.resume_parser import ResumeParserError, extract_text_from_resume
from app.services.matcher import (
    calculate_match_percentage,
    get_matched_skills,
    get_missing_skills,
)
from app.services.recruiter_matcher import build_recruiter_analysis
from app.services.similarity import calculate_tfidf_similarity
from app.services.skill_extractor import extract_skills
from app.services.suggestion_engine import generate_suggestions
from app.utils.text_cleaner import clean_text


app = FastAPI(title="AI Resume Matcher API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    return {
        "message": "AI Resume Matcher API is running.",
        "phase": "Phase 1 - Resume parsing and text extraction",
    }


@app.post("/extract-text")
async def extract_resume_text(resume: UploadFile = File(...)) -> dict:
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    allowed_extensions = {".pdf", ".docx"}

    filename = resume.filename or ""
    extension = "." + filename.split(".")[-1].lower() if "." in filename else ""

    if not filename:
        raise HTTPException(status_code=400, detail="Resume filename is required.")

    if resume.content_type not in allowed_types and extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF or DOCX resume.",
        )

    file_bytes = await resume.read()

    try:
        extracted_text = extract_text_from_resume(filename=filename, file_bytes=file_bytes)
    except ResumeParserError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract text from the uploaded resume.",
        ) from exc

    cleaned_text = clean_text(extracted_text)

    return {
        "filename": filename,
        "raw_text": extracted_text,
        "cleaned_text": cleaned_text,
        "character_count": len(cleaned_text),
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> dict:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    extract_response = await extract_resume_text(resume)
    resume_text = extract_response["cleaned_text"]
    cleaned_job_description = clean_text(job_description)

    resume_skills = extract_skills(resume_text)
    job_description_skills = extract_skills(cleaned_job_description)
    matched_skills = get_matched_skills(resume_skills, job_description_skills)
    missing_skills = get_missing_skills(resume_skills, job_description_skills)
    tfidf_similarity = calculate_tfidf_similarity(resume_text, cleaned_job_description)
    recruiter_analysis = build_recruiter_analysis(
        resume_text=resume_text,
        job_description_text=cleaned_job_description,
        resume_skills=resume_skills,
        job_description_skills=job_description_skills,
        tfidf_similarity=tfidf_similarity,
    )

    return {
        "match_percentage": recruiter_analysis["overall_match_percentage"],
        "overall_match_percentage": recruiter_analysis["overall_match_percentage"],
        "skill_match_percentage": recruiter_analysis["skill_match_percentage"],
        "experience_match_percentage": recruiter_analysis["experience_match_percentage"],
        "education_match_percentage": recruiter_analysis["education_match_percentage"],
        "certification_match_percentage": recruiter_analysis["certification_match_percentage"],
        "eligibility_match_percentage": recruiter_analysis["eligibility_match_percentage"],
        "tfidf_similarity": tfidf_similarity,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_education": recruiter_analysis["matched_education"],
        "missing_education": recruiter_analysis["missing_education"],
        "matched_certifications": recruiter_analysis["matched_certifications"],
        "missing_certifications": recruiter_analysis["missing_certifications"],
        "required_experience_years": recruiter_analysis["required_experience_years"],
        "resume_experience_years": recruiter_analysis["resume_experience_years"],
        "criteria_breakdown": recruiter_analysis["criteria_breakdown"],
        "suggestions": generate_suggestions(
            missing_skills=missing_skills,
            tfidf_similarity=tfidf_similarity,
            required_experience_years=recruiter_analysis["required_experience_years"],
            resume_experience_years=recruiter_analysis["resume_experience_years"],
            missing_education=recruiter_analysis["missing_education"],
            missing_certifications=recruiter_analysis["missing_certifications"],
        ),
        "resume_skills": resume_skills,
        "job_description_skills": job_description_skills,
    }
