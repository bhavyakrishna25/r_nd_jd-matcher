import re

from app.data.skills import SKILL_KEYWORDS


def _build_skill_pattern(skill: str) -> re.Pattern[str]:
    escaped_skill = re.escape(skill)
    escaped_skill = escaped_skill.replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\w){escaped_skill}(?!\w)", re.IGNORECASE)


SKILL_PATTERNS = {skill: _build_skill_pattern(skill) for skill in SKILL_KEYWORDS}


def extract_skills(text: str) -> list[str]:
    found_skills = [
        skill
        for skill, pattern in SKILL_PATTERNS.items()
        if pattern.search(text)
    ]
    return sorted(found_skills)
