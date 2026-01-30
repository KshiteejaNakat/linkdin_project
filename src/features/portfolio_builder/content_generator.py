"""
Portfolio Content Generator Module
Generates content for portfolio sections.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class HeroContent:
    """Hero section content."""
    name: str
    title: str
    tagline: str
    description: str
    cta_primary: str = "View My Work"
    cta_secondary: str = "Contact Me"
    image_url: Optional[str] = None


@dataclass
class ProjectContent:
    """Project section content."""
    title: str
    description: str
    technologies: List[str]
    image_url: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    highlights: List[str] = field(default_factory=list)


@dataclass
class PortfolioContent:
    """Complete portfolio content."""
    hero: HeroContent
    about: str
    skills: Dict[str, List[str]]
    projects: List[ProjectContent]
    experience: List[Dict]
    education: List[Dict]
    contact: Dict[str, str]
    testimonials: List[Dict] = field(default_factory=list)


class PortfolioContentGenerator:
    """
    Generates compelling content for portfolio sections
    based on user career DNA and market patterns.
    """
    
    def __init__(self, llm_client: Any = None):
        self.llm_client = llm_client
        
    async def generate_portfolio_content(
        self,
        career_dna: Dict,
        user_data: Dict,
        style: str = "professional"
    ) -> PortfolioContent:
        """Generate complete portfolio content."""
        
        hero = self._generate_hero(career_dna, user_data, style)
        about = await self._generate_about(career_dna, user_data, style)
        skills = self._organize_skills(career_dna, user_data)
        projects = self._format_projects(career_dna, user_data)
        experience = self._format_experience(user_data)
        education = self._format_education(user_data)
        contact = self._format_contact(user_data)
        
        return PortfolioContent(
            hero=hero,
            about=about,
            skills=skills,
            projects=projects,
            experience=experience,
            education=education,
            contact=contact
        )
    
    def _generate_hero(
        self, career_dna: Dict, user_data: Dict, style: str
    ) -> HeroContent:
        """Generate hero section content."""
        name = user_data.get("name", career_dna.get("name", ""))
        role = user_data.get("target_role", career_dna.get("target_role", "Professional"))
        
        tagline = self._create_tagline(career_dna, user_data)
        description = self._create_hero_description(career_dna, user_data)
        
        return HeroContent(
            name=name,
            title=role,
            tagline=tagline,
            description=description,
            cta_primary="Explore My Work",
            cta_secondary="Get In Touch"
        )
    
    def _create_tagline(self, career_dna: Dict, user_data: Dict) -> str:
        """Create compelling tagline."""
        role = user_data.get("target_role", "Professional")
        strengths = career_dna.get("strengths", [])
        industry = user_data.get("industry", "technology")
        
        if strengths:
            return f"{role} • {strengths[0]} • {industry.title()}"
        
        return f"Passionate {role} Building Impactful Solutions"
    
    def _create_hero_description(self, career_dna: Dict, user_data: Dict) -> str:
        """Create hero description text."""
        value_prop = career_dna.get("value_proposition", "")
        if value_prop:
            return value_prop
        
        role = user_data.get("target_role", "professional")
        industry = user_data.get("industry", "technology")
        
        return f"I'm a {role} passionate about creating innovative solutions in {industry}. I combine technical expertise with strategic thinking to deliver impactful results."
    
    async def _generate_about(
        self, career_dna: Dict, user_data: Dict, style: str
    ) -> str:
        """Generate about section content."""
        if self.llm_client:
            return await self._generate_about_llm(career_dna, user_data, style)
        
        return self._generate_about_template(career_dna, user_data, style)
    
    def _generate_about_template(
        self, career_dna: Dict, user_data: Dict, style: str
    ) -> str:
        """Generate about content from template."""
        name = user_data.get("name", "")
        role = user_data.get("target_role", "professional")
        years = user_data.get("years_experience", career_dna.get("years_experience", 5))
        industry = user_data.get("industry", "technology")
        
        strengths = career_dna.get("strengths", [])
        strength_text = ", ".join(strengths[:3]) if strengths else "problem-solving"
        
        return f"""With {years}+ years of experience as a {role} in {industry}, I specialize in {strength_text}.

My journey has been driven by a passion for solving complex challenges and delivering measurable impact. I believe in the power of continuous learning and collaboration to achieve exceptional results.

When I'm not working, you can find me exploring new technologies, contributing to open source, and sharing knowledge with the community."""
    
    async def _generate_about_llm(
        self, career_dna: Dict, user_data: Dict, style: str
    ) -> str:
        """Generate about content using LLM."""
        prompt = f"""Write a compelling portfolio About section:

Role: {user_data.get('target_role', 'Professional')}
Industry: {user_data.get('industry', 'Technology')}
Years Experience: {user_data.get('years_experience', 5)}
Strengths: {', '.join(career_dna.get('strengths', [])[:3])}
Style: {style}

Requirements:
- 150-200 words
- Engaging and authentic
- Highlight unique value
- Personal touch

Write the about section:"""
        
        try:
            return await self.llm_client.generate(prompt)
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return self._generate_about_template(career_dna, user_data, style)
    
    def _organize_skills(self, career_dna: Dict, user_data: Dict) -> Dict[str, List[str]]:
        """Organize skills for portfolio display."""
        skills_data = career_dna.get("skills", {})
        
        if isinstance(skills_data, dict):
            return {
                "Technical": skills_data.get("technical", [])[:8],
                "Tools & Platforms": skills_data.get("tools", [])[:6],
                "Languages": skills_data.get("languages", [])[:5],
                "Soft Skills": skills_data.get("soft", [])[:4]
            }
        
        # If skills is a list
        all_skills = user_data.get("skills", [])
        return {"All Skills": all_skills[:15]}
    
    def _format_projects(
        self, career_dna: Dict, user_data: Dict
    ) -> List[ProjectContent]:
        """Format projects for portfolio."""
        projects = career_dna.get("projects", user_data.get("projects", []))
        
        formatted = []
        for proj in projects[:6]:
            formatted.append(ProjectContent(
                title=proj.get("name", proj.get("title", "")),
                description=proj.get("description", ""),
                technologies=proj.get("technologies", []),
                github_url=proj.get("url", proj.get("github_url", "")),
                live_url=proj.get("live_url", ""),
                highlights=proj.get("highlights", [])
            ))
        
        return formatted
    
    def _format_experience(self, user_data: Dict) -> List[Dict]:
        """Format experience for portfolio timeline."""
        experience = user_data.get("experience", [])
        
        formatted = []
        for exp in experience[:5]:
            formatted.append({
                "title": exp.get("title", ""),
                "company": exp.get("company", ""),
                "period": exp.get("period", ""),
                "description": exp.get("description", ""),
                "highlights": exp.get("bullets", [])[:3]
            })
        
        return formatted
    
    def _format_education(self, user_data: Dict) -> List[Dict]:
        """Format education for portfolio."""
        education = user_data.get("education", [])
        
        formatted = []
        for edu in education[:3]:
            formatted.append({
                "degree": edu.get("degree", ""),
                "institution": edu.get("institution", edu.get("school", "")),
                "period": edu.get("period", edu.get("year", "")),
                "details": edu.get("details", "")
            })
        
        return formatted
    
    def _format_contact(self, user_data: Dict) -> Dict[str, str]:
        """Format contact information."""
        return {
            "email": user_data.get("email", ""),
            "linkedin": user_data.get("linkedin_url", ""),
            "github": user_data.get("github_url", ""),
            "twitter": user_data.get("twitter_url", ""),
            "website": user_data.get("website", ""),
            "location": user_data.get("location", "")
        }
