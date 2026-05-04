export interface CriteriaBreakdownItem {
  criterion: string;
  score: number;
  status: string;
  details: string;
}

export interface AnalysisResult {
  match_percentage: number;
  overall_match_percentage: number;
  skill_match_percentage: number;
  experience_match_percentage: number;
  education_match_percentage: number;
  certification_match_percentage: number;
  eligibility_match_percentage: number;
  tfidf_similarity: number;
  matched_skills: string[];
  missing_skills: string[];
  matched_education: string[];
  missing_education: string[];
  matched_certifications: string[];
  missing_certifications: string[];
  required_experience_years: number | null;
  resume_experience_years: number;
  criteria_breakdown: CriteriaBreakdownItem[];
  suggestions: string[];
  resume_skills: string[];
  job_description_skills: string[];
}
