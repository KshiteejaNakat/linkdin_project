"""
About Section Generator Module
Generates compelling LinkedIn About sections.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class AboutResult:
    """Result of about section generation."""
    content: str
    word_count: int
    score: int
    structure: List[str]
    suggestions: List[str]


class AboutGenerator:
    """
    Generates compelling LinkedIn About sections based on
    user career DNA and market patterns.
    """
    
    OPTIMAL_WORD_COUNT = (200, 350)
    
    def __init__(self, llm_client: Any = None):
        self.llm_client = llm_client
        
    async def generate(
        self,
        user_data: Dict[str, Any],
        career_dna: Optional[Dict] = None,
        tone: str = "professional"
    ) -> AboutResult:
        """Generate optimized About section."""
        
        if self.llm_client:
            content = await self._generate_with_llm(user_data, career_dna, tone)
        else:
            content = self._generate_from_template(user_data, career_dna, tone)
        
        return self._score_about(content, user_data)
    
    def _generate_from_template(
        self,
        user_data: Dict,
        career_dna: Optional[Dict],
        tone: str
    ) -> str:
        """Generate About section from templates."""
        name = user_data.get("name", "")
        role = user_data.get("target_role", user_data.get("current_role", "professional"))
        industry = user_data.get("industry", "technology")
        years_exp = user_data.get("years_experience", "several")
        
        # Get strengths and skills
        strengths = []
        if career_dna:
            strengths = career_dna.get("strengths", [])
        
        skills = user_data.get("top_skills", [])[:5]
        achievements = user_data.get("achievements", [])
        
        # Build About section
        sections = []
        
        # Hook/Opening
        opening = self._generate_opening(role, industry, tone)
        sections.append(opening)
        
        # Value proposition
        value_prop = self._generate_value_section(role, skills, years_exp)
        sections.append(value_prop)
        
        # Achievements/Impact
        if achievements:
            impact_section = self._generate_impact_section(achievements)
            sections.append(impact_section)
        
        # Skills highlight
        if skills:
            skills_section = self._generate_skills_section(skills)
            sections.append(skills_section)
        
        # Call to action
        cta = self._generate_cta(user_data)
        sections.append(cta)
        
        return "\n\n".join(sections)
    
    def _generate_opening(self, role: str, industry: str, tone: str) -> str:
        """Generate compelling opening hook."""
        openings = {
            "professional": f"As a {role} in {industry}, I'm driven by the challenge of solving complex problems and delivering measurable results.",
            "conversational": f"Hi! I'm a {role} who loves turning ideas into reality. Working in {industry} has taught me that the best solutions come from collaboration and curiosity.",
            "impactful": f"Transforming challenges into opportunities is what drives me. With deep expertise in {industry}, I help organizations achieve their most ambitious goals."
        }
        
        return openings.get(tone, openings["professional"])
    
    def _generate_value_section(
        self, role: str, skills: List[str], years_exp: Any
    ) -> str:
        """Generate value proposition section."""
        skill_text = ", ".join(skills[:3]) if skills else "strategic thinking"
        
        return f"""With {years_exp} years of experience, I bring expertise in {skill_text}. My approach combines analytical rigor with creative problem-solving to drive meaningful outcomes.

What sets me apart is my ability to bridge the gap between technical execution and business strategy, ensuring that every solution creates lasting value."""
    
    def _generate_impact_section(self, achievements: List[str]) -> str:
        """Generate impact/achievements section."""
        achievement_bullets = "\n".join([f"• {a}" for a in achievements[:4]])
        
        return f"""Key achievements include:

{achievement_bullets}"""
    
    def _generate_skills_section(self, skills: List[str]) -> str:
        """Generate skills highlight section."""
        skills_text = " | ".join(skills[:6])
        
        return f"""Core competencies:
{skills_text}"""
    
    def _generate_cta(self, user_data: Dict) -> str:
        """Generate call-to-action."""
        email = user_data.get("email", "")
        
        cta = "I'm always interested in connecting with fellow professionals and exploring new opportunities. Whether you're looking to collaborate, discuss industry trends, or explore potential synergies, feel free to reach out!"
        
        if email:
            cta += f"\n\n📧 {email}"
        
        return cta
    
    async def _generate_with_llm(
        self,
        user_data: Dict,
        career_dna: Optional[Dict],
        tone: str
    ) -> str:
        """Generate About section using LLM."""
        prompt = self._build_llm_prompt(user_data, career_dna, tone)
        
        try:
            response = await self.llm_client.generate(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return self._generate_from_template(user_data, career_dna, tone)
    
    def _build_llm_prompt(
        self, user_data: Dict, career_dna: Optional[Dict], tone: str
    ) -> str:
        """Build prompt for LLM generation."""
        strengths = career_dna.get("strengths", []) if career_dna else []
        
        return f"""Write a compelling LinkedIn About section for:

Name: {user_data.get('name', 'Professional')}
Current Role: {user_data.get('current_role', '')}
Target Role: {user_data.get('target_role', '')}
Industry: {user_data.get('industry', 'Technology')}
Years of Experience: {user_data.get('years_experience', '5+')}
Top Skills: {', '.join(user_data.get('top_skills', [])[:5])}
Key Strengths: {', '.join(strengths[:3])}
Achievements: {', '.join(user_data.get('achievements', [])[:3])}

Tone: {tone}

Requirements:
- 200-350 words
- Start with a compelling hook
- Include value proposition
- Mention key achievements with metrics if available
- End with a call-to-action
- Use first person perspective
- Be authentic and specific

Write the About section:"""
    
    def _score_about(self, content: str, user_data: Dict) -> AboutResult:
        """Score the About section quality."""
        score = 0
        structure = []
        suggestions = []
        
        word_count = len(content.split())
        
        # Word count scoring
        if self.OPTIMAL_WORD_COUNT[0] <= word_count <= self.OPTIMAL_WORD_COUNT[1]:
            score += 25
            structure.append("optimal_length")
        elif word_count < self.OPTIMAL_WORD_COUNT[0]:
            suggestions.append("Consider expanding your About section")
            score += 10
        else:
            suggestions.append("Consider condensing for better readability")
            score += 15
        
        # Structure scoring
        paragraphs = content.split("\n\n")
        if len(paragraphs) >= 3:
            score += 15
            structure.append("good_structure")
        
        # Opening hook
        first_line = content.split(".")[0] if content else ""
        if len(first_line) > 20:
            score += 10
            structure.append("has_hook")
        
        # Call to action
        cta_keywords = ["reach out", "connect", "contact", "email", "let's chat"]
        if any(kw in content.lower() for kw in cta_keywords):
            score += 15
            structure.append("has_cta")
        else:
            suggestions.append("Add a call-to-action")
        
        # Skills mentioned
        skills = user_data.get("top_skills", [])
        skills_mentioned = sum(1 for s in skills if s.lower() in content.lower())
        score += min(skills_mentioned * 5, 15)
        if skills_mentioned:
            structure.append("skills_mentioned")
        
        # Achievements
        if any(char.isdigit() for char in content):
            score += 10
            structure.append("has_metrics")
        else:
            suggestions.append("Add quantifiable achievements")
        
        # First person
        if content.lower().startswith("i ") or " I " in content:
            score += 10
            structure.append("first_person")
        
        return AboutResult(
            content=content,
            word_count=word_count,
            score=min(score, 100),
            structure=structure,
            suggestions=suggestions
        )
    
    def improve_existing(
        self, current_about: str, user_data: Dict
    ) -> List[str]:
        """Generate improvement suggestions for existing About."""
        result = self._score_about(current_about, user_data)
        return result.suggestions
