def generate_suggestions(
    missing_skills: list[str],
    tfidf_similarity: float,
    required_experience_years: int | None,
    resume_experience_years: int,
    missing_education: list[str],
    missing_certifications: list[str],
) -> list[str]:
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Add {skill.title()} experience to your resume.")
        suggestions.append(f"Learn {skill.title()} to improve your match.")

    if required_experience_years is not None and resume_experience_years < required_experience_years:
        suggestions.append(
            f"Show stronger proof of {required_experience_years}+ years of relevant experience in your resume."
        )

    for education_keyword in missing_education[:2]:
        suggestions.append(f"If applicable, highlight your {education_keyword.title()} qualification clearly.")

    for certification_keyword in missing_certifications[:2]:
        suggestions.append(f"If applicable, add your {certification_keyword.title()} certification to the resume.")

    if tfidf_similarity < 40:
        suggestions.append("Rewrite your resume summary so it mirrors the job description more closely.")
    elif tfidf_similarity < 70:
        suggestions.append("Use more job-specific keywords in your project and experience sections.")

    return suggestions[:6]
