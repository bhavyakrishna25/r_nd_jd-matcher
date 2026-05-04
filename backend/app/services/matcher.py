def calculate_match_percentage(
    resume_skills: list[str],
    job_description_skills: list[str],
) -> float:
    if not job_description_skills:
        return 0.0

    matched_skills = set(resume_skills) & set(job_description_skills)
    return round((len(matched_skills) / len(set(job_description_skills))) * 100, 2)


def get_matched_skills(resume_skills: list[str], job_description_skills: list[str]) -> list[str]:
    return sorted(set(resume_skills) & set(job_description_skills))


def get_missing_skills(resume_skills: list[str], job_description_skills: list[str]) -> list[str]:
    return sorted(set(job_description_skills) - set(resume_skills))
