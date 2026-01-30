"""
Career DNA Builder Module
Constructs a comprehensive career profile from multiple data sources.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger

from .resume_parser import ParsedResume
from .github_analyzer import GitHubProfile


@dataclass
class CareerDNA:
    """Complete career DNA profile."""
    name: str
    email: str
    current_role: str
    target_role: str
    industry: str
    years_experience: int
    
    # Core strengths
    strengths: List[str] = field(default_factory=list)
    
    # Skill analysis
    skills: Dict[str, List[str]] = field(default_factory=dict)
    skill_gaps: List[str] = field(default_factory=list)
    
    # Experience
    experience: List[Dict] = field(default_factory=list)
    education: List[Dict] = field(default_factory=list)
    
    # Projects
    projects: List[Dict] = field(default_factory=list)
    
    # Career insights
    value_proposition: str = ""
    unique_differentiators: List[str] = field(default_factory=list)
    growth_opportunities: List[str] = field(default_factory=list)
    
    # Scores
    profile_score: int = 0
    market_alignment: int = 0


class CareerDNABuilder:
    """
    Builds comprehensive career DNA by combining data from
    multiple sources (resume, LinkedIn, GitHub).
    """
    
    def __init__(self):
        self.weights = {
            "experience": 0.30,
            "skills": 0.25,
            "projects": 0.20,
            "education": 0.15,
            "presence": 0.10
        }
    
    async def build_dna(
        self,
        resume: Optional[ParsedResume] = None,
        linkedin_data: Optional[Dict] = None,
        github_profile: Optional[GitHubProfile] = None,
        user_input: Optional[Dict] = None
    ) -> CareerDNA:
        """Build career DNA from available data sources."""
        logger.info("Building career DNA...")
        
        # Merge data from all sources
        merged_data = self._merge_data_sources(
            resume, linkedin_data, github_profile, user_input
        )
        
        # Build career DNA
        dna = CareerDNA(
            name=merged_data.get("name", ""),
            email=merged_data.get("email", ""),
            current_role=merged_data.get("current_role", ""),
            target_role=merged_data.get("target_role", ""),
            industry=merged_data.get("industry", ""),
            years_experience=self._calculate_years(merged_data.get("experience", []))
        )
        
        # Analyze and populate fields
        dna.strengths = self._identify_strengths(merged_data)
        dna.skills = self._organize_skills(merged_data)
        dna.skill_gaps = self._identify_gaps(merged_data)
        dna.experience = merged_data.get("experience", [])
        dna.education = merged_data.get("education", [])
        dna.projects = self._format_projects(merged_data)
        dna.value_proposition = self._generate_value_prop(merged_data)
        dna.unique_differentiators = self._find_differentiators(merged_data)
        dna.growth_opportunities = self._identify_opportunities(merged_data)
        dna.profile_score = self._calculate_profile_score(dna)
        dna.market_alignment = self._calculate_market_alignment(dna)
        
        return dna
    
    def _merge_data_sources(
        self,
        resume: Optional[ParsedResume],
        linkedin: Optional[Dict],
        github: Optional[GitHubProfile],
        user_input: Optional[Dict]
    ) -> Dict[str, Any]:
        """Merge data from multiple sources with priority."""
        merged = {}
        
        # User input has highest priority
        if user_input:
            merged.update(user_input)
        
        # Resume data
        if resume:
            merged.setdefault("name", resume.name)
            merged.setdefault("email", resume.email)
            merged.setdefault("experience", resume.experience)
            merged.setdefault("education", resume.education)
            merged.setdefault("summary", resume.summary)
            
            # Merge skills
            merged_skills = merged.get("skills", [])
            merged_skills.extend(resume.skills)
            merged["skills"] = list(set(merged_skills))
            
            # Merge projects
            merged_projects = merged.get("projects", [])
            merged_projects.extend(resume.projects)
            merged["projects"] = merged_projects
        
        # LinkedIn data
        if linkedin:
            merged.setdefault("name", linkedin.get("name", ""))
            merged.setdefault("headline", linkedin.get("headline", ""))
            merged.setdefault("about", linkedin.get("about", ""))
            merged.setdefault("current_role", self._extract_current_role(linkedin))
            
            # Merge skills
            linkedin_skills = linkedin.get("skills", [])
            skill_names = [s.get("name", s) if isinstance(s, dict) else s for s in linkedin_skills]
            merged_skills = merged.get("skills", [])
            merged_skills.extend(skill_names)
            merged["skills"] = list(set(merged_skills))
        
        # GitHub data
        if github:
            merged.setdefault("github_username", github.username)
            merged["github_languages"] = github.top_languages
            merged["github_contribution_score"] = github.contribution_score
            
            # Add GitHub projects
            github_projects = [
                {
                    "name": p.name,
                    "description": p.description,
                    "technologies": [p.language] + p.topics[:3],
                    "url": p.url,
                    "source": "github"
                }
                for p in github.projects[:5]
            ]
            merged_projects = merged.get("projects", [])
            merged_projects.extend(github_projects)
            merged["projects"] = merged_projects
        
        return merged
    
    def _calculate_years(self, experience: List[Dict]) -> int:
        """Calculate total years of experience."""
        # Simplified calculation
        return len(experience) * 2 if experience else 0
    
    def _identify_strengths(self, data: Dict) -> List[str]:
        """Identify top strengths from data."""
        strengths = []
        
        # From skills
        skills = data.get("skills", [])
        if len(skills) >= 10:
            strengths.append("Diverse skill set")
        
        # From experience
        experience = data.get("experience", [])
        if len(experience) >= 3:
            strengths.append("Strong work history")
        
        # From projects
        projects = data.get("projects", [])
        if len(projects) >= 5:
            strengths.append("Proven project delivery")
        
        # From GitHub
        if data.get("github_contribution_score", 0) > 50:
            strengths.append("Active open source contributor")
        
        return strengths
    
    def _organize_skills(self, data: Dict) -> Dict[str, List[str]]:
        """Organize skills into categories."""
        skills = data.get("skills", [])
        github_languages = data.get("github_languages", [])
        
        organized = {
            "technical": [],
            "soft": [],
            "tools": [],
            "languages": list(set(github_languages))
        }
        
        technical_keywords = ["python", "java", "sql", "aws", "docker", "kubernetes"]
        soft_keywords = ["leadership", "communication", "teamwork", "problem"]
        tool_keywords = ["excel", "jira", "git", "tableau", "figma"]
        
        for skill in skills:
            skill_lower = skill.lower() if isinstance(skill, str) else ""
            
            if any(kw in skill_lower for kw in technical_keywords):
                organized["technical"].append(skill)
            elif any(kw in skill_lower for kw in soft_keywords):
                organized["soft"].append(skill)
            elif any(kw in skill_lower for kw in tool_keywords):
                organized["tools"].append(skill)
            else:
                organized["technical"].append(skill)
        
        return organized
    
    def _identify_gaps(self, data: Dict) -> List[str]:
        """Identify skill gaps for target role."""
        target_role = data.get("target_role", "").lower()
        current_skills = set(s.lower() for s in data.get("skills", []))
        
        # Common requirements by role type
        role_requirements = {
            "software engineer": ["python", "git", "sql", "aws"],
            "data scientist": ["python", "sql", "machine learning", "statistics"],
            "product manager": ["product strategy", "roadmapping", "analytics"]
        }
        
        required = []
        for role, skills in role_requirements.items():
            if role in target_role:
                required = skills
                break
        
        gaps = [s for s in required if s.lower() not in current_skills]
        return gaps
    
    def _format_projects(self, data: Dict) -> List[Dict]:
        """Format and deduplicate projects."""
        projects = data.get("projects", [])
        
        seen_names = set()
        unique_projects = []
        
        for project in projects:
            name = project.get("name", "").lower()
            if name not in seen_names:
                seen_names.add(name)
                unique_projects.append(project)
        
        return unique_projects[:10]
    
    def _generate_value_prop(self, data: Dict) -> str:
        """Generate value proposition statement."""
        role = data.get("target_role", "professional")
        strengths = self._identify_strengths(data)
        industry = data.get("industry", "technology")
        
        strength_text = strengths[0] if strengths else "expertise"
        
        return f"A {role} with {strength_text}, driving impact in {industry}"
    
    def _find_differentiators(self, data: Dict) -> List[str]:
        """Find unique differentiators."""
        differentiators = []
        
        # Unique skill combinations
        skills = data.get("skills", [])
        if "python" in [s.lower() for s in skills] and "leadership" in [s.lower() for s in skills]:
            differentiators.append("Technical expertise with leadership skills")
        
        # GitHub presence
        if data.get("github_contribution_score", 0) > 70:
            differentiators.append("Strong open source contributions")
        
        # Project variety
        projects = data.get("projects", [])
        if len(projects) > 5:
            differentiators.append("Diverse project portfolio")
        
        return differentiators
    
    def _identify_opportunities(self, data: Dict) -> List[str]:
        """Identify growth opportunities."""
        opportunities = []
        gaps = self._identify_gaps(data)
        
        for gap in gaps[:3]:
            opportunities.append(f"Learn {gap} to strengthen profile")
        
        if not data.get("certifications"):
            opportunities.append("Add industry certifications")
        
        return opportunities
    
    def _calculate_profile_score(self, dna: CareerDNA) -> int:
        """Calculate overall profile completeness score."""
        score = 0
        
        # Basic info
        if dna.name:
            score += 10
        if dna.email:
            score += 5
        
        # Experience
        score += min(len(dna.experience) * 10, 30)
        
        # Skills
        total_skills = sum(len(v) for v in dna.skills.values())
        score += min(total_skills * 2, 25)
        
        # Projects
        score += min(len(dna.projects) * 5, 20)
        
        # Education
        score += min(len(dna.education) * 5, 10)
        
        return min(score, 100)
    
    def _calculate_market_alignment(self, dna: CareerDNA) -> int:
        """Calculate alignment with market demands."""
        score = 50  # Base score
        
        # Adjust based on gaps
        score -= len(dna.skill_gaps) * 5
        
        # Adjust based on strengths
        score += len(dna.strengths) * 5
        
        return max(0, min(score, 100))
    
    def _extract_current_role(self, linkedin: Dict) -> str:
        """Extract current role from LinkedIn data."""
        experience = linkedin.get("experience", [])
        if experience:
            return experience[0].get("title", "")
        return linkedin.get("headline", "").split("|")[0].strip()
