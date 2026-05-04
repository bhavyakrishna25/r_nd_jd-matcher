from app.services.criteria_extractor import (
    extract_certification_keywords,
    extract_education_keywords,
    extract_eligibility_keywords,
    extract_required_experience_years,
    extract_resume_experience_years,
)
from app.services.matcher import calculate_match_percentage


def _ratio_score(matched_items: list[str], required_items: list[str]) -> float:
    if not required_items:
        return 100.0

    return round((len(set(matched_items)) / len(set(required_items))) * 100, 2)


def _experience_score(required_years: int | None, resume_years: int) -> float:
    if required_years is None:
        return 100.0

    if required_years == 0:
        return 100.0

    return round(min(resume_years / required_years, 1) * 100, 2)


def _criteria_status(score: float) -> str:
    if score >= 80:
        return "strong"
    if score >= 50:
        return "moderate"
    return "gap"


def build_recruiter_analysis(
    resume_text: str,
    job_description_text: str,
    resume_skills: list[str],
    job_description_skills: list[str],
    tfidf_similarity: float,
) -> dict:
    resume_education = extract_education_keywords(resume_text)
    job_education = extract_education_keywords(job_description_text)
    resume_certifications = extract_certification_keywords(resume_text)
    job_certifications = extract_certification_keywords(job_description_text)
    resume_eligibility = extract_eligibility_keywords(resume_text)
    job_eligibility = extract_eligibility_keywords(job_description_text)

    required_experience_years = extract_required_experience_years(job_description_text)
    resume_experience_years = extract_resume_experience_years(resume_text)

    matched_education = sorted(set(resume_education) & set(job_education))
    missing_education = sorted(set(job_education) - set(resume_education))
    matched_certifications = sorted(set(resume_certifications) & set(job_certifications))
    missing_certifications = sorted(set(job_certifications) - set(resume_certifications))
    matched_eligibility = sorted(set(resume_eligibility) & set(job_eligibility))
    missing_eligibility = sorted(set(job_eligibility) - set(resume_eligibility))

    skill_match_percentage = calculate_match_percentage(resume_skills, job_description_skills)
    experience_match_percentage = _experience_score(required_experience_years, resume_experience_years)
    education_match_percentage = _ratio_score(matched_education, job_education)
    certification_match_percentage = _ratio_score(matched_certifications, job_certifications)
    eligibility_match_percentage = _ratio_score(matched_eligibility, job_eligibility)

    weighted_score = (
        skill_match_percentage * 0.45
        + experience_match_percentage * 0.2
        + education_match_percentage * 0.1
        + certification_match_percentage * 0.1
        + eligibility_match_percentage * 0.05
        + tfidf_similarity * 0.1
    )

    criteria_breakdown = [
        {
            "criterion": "Skills",
            "score": round(skill_match_percentage, 2),
            "status": _criteria_status(skill_match_percentage),
            "details": f"Matched {len(set(resume_skills) & set(job_description_skills))} of {len(set(job_description_skills)) or 0} job skills.",
        },
        {
            "criterion": "Experience",
            "score": round(experience_match_percentage, 2),
            "status": _criteria_status(experience_match_percentage),
            "details": (
                f"JD asks for {required_experience_years}+ years and resume shows about {resume_experience_years} years."
                if required_experience_years is not None
                else f"No clear experience threshold found in JD. Resume shows about {resume_experience_years} years."
            ),
        },
        {
            "criterion": "Education",
            "score": round(education_match_percentage, 2),
            "status": _criteria_status(education_match_percentage),
            "details": (
                f"Matched education keywords: {', '.join(matched_education)}."
                if matched_education
                else "No direct education keyword match found."
            ),
        },
        {
            "criterion": "Certifications",
            "score": round(certification_match_percentage, 2),
            "status": _criteria_status(certification_match_percentage),
            "details": (
                f"Matched certifications: {', '.join(matched_certifications)}."
                if matched_certifications
                else "No direct certification match found."
            ),
        },
        {
            "criterion": "Overall JD Alignment",
            "score": round(tfidf_similarity, 2),
            "status": _criteria_status(tfidf_similarity),
            "details": "Measures how closely the resume wording aligns with the job description.",
        },
    ]

    return {
        "overall_match_percentage": round(weighted_score, 2),
        "skill_match_percentage": round(skill_match_percentage, 2),
        "experience_match_percentage": round(experience_match_percentage, 2),
        "education_match_percentage": round(education_match_percentage, 2),
        "certification_match_percentage": round(certification_match_percentage, 2),
        "eligibility_match_percentage": round(eligibility_match_percentage, 2),
        "required_experience_years": required_experience_years,
        "resume_experience_years": resume_experience_years,
        "matched_education": matched_education,
        "missing_education": missing_education,
        "matched_certifications": matched_certifications,
        "missing_certifications": missing_certifications,
        "matched_eligibility": matched_eligibility,
        "missing_eligibility": missing_eligibility,
        "criteria_breakdown": criteria_breakdown,
    }
