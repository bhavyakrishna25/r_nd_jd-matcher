import re

from app.data.criteria import CERTIFICATION_KEYWORDS, DEGREE_KEYWORDS, ELIGIBILITY_KEYWORDS


def _extract_keyword_matches(text: str, keywords: list[str]) -> list[str]:
    found_keywords = []

    for keyword in keywords:
        pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", re.IGNORECASE)
        if pattern.search(text):
            found_keywords.append(keyword)

    return sorted(found_keywords)


def extract_education_keywords(text: str) -> list[str]:
    return _extract_keyword_matches(text, DEGREE_KEYWORDS)


def extract_certification_keywords(text: str) -> list[str]:
    return _extract_keyword_matches(text, CERTIFICATION_KEYWORDS)


def extract_eligibility_keywords(text: str) -> list[str]:
    return _extract_keyword_matches(text, ELIGIBILITY_KEYWORDS)


def extract_required_experience_years(text: str) -> int | None:
    year_patterns = [
        r"(\d+)\+?\s+years?\s+of\s+experience",
        r"minimum\s+(\d+)\s+years?",
        r"at\s+least\s+(\d+)\s+years?",
        r"(\d+)\s*-\s*\d+\s+years?",
    ]

    extracted_years = []
    for pattern in year_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        extracted_years.extend(int(match) for match in matches)

    if not extracted_years:
        return None

    return max(extracted_years)


def extract_resume_experience_years(text: str) -> int:
    year_patterns = [
        r"(\d+)\+?\s+years?\s+of\s+experience",
        r"(\d+)\+?\s+years?\s+experience",
        r"experience\s+of\s+(\d+)\+?\s+years?",
    ]

    extracted_years = []
    for pattern in year_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        extracted_years.extend(int(match) for match in matches)

    return max(extracted_years) if extracted_years else 0
