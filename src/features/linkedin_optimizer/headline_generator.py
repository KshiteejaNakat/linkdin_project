"""
Headline Generator Module
Generates optimized LinkedIn headlines using market patterns.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class HeadlineResult:
    """Result of headline generation."""
    headline: str
    score: int
    patterns_used: List[str]
    character_count: int
    suggestions: List[str]


class HeadlineGenerator:
    """
    Generates compelling LinkedIn headlines based on
    market patterns and user profile data.
    """
    
    MAX_LENGTH = 220  # LinkedIn headline max length
    OPTIMAL_LENGTH = (80, 150)
    
    def __init__(self, llm_client: Any = None):
        self.llm_client = llm_client
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """Load headline templates by role type."""
        return {
            "developer": "{role} | Building {specialty} | {company_or_value}",
            "analyst": "{role} | Transforming Data into {outcome} | {industry}",
            "manager": "{role} | Leading Teams to {achievement} | {company_or_industry}",
            "designer": "{role} | Crafting {specialty} Experiences | {focus}",
            "default": "{role} | {specialty} | {value_proposition}"
        }
    
    async def generate(
        self,
        user_data: Dict[str, Any],
        market_patterns: Optional[Dict] = None,
        num_variants: int = 3
    ) -> List[HeadlineResult]:
        """Generate optimized headline variants."""
        role = user_data.get("target_role", user_data.get("current_role", "Professional"))
        
        variants = []
        
        # Generate template-based variants
        template_variants = self._generate_from_templates(user_data)
        variants.extend(template_variants)
        
        # Generate pattern-based variants
        if market_patterns:
            pattern_variants = self._generate_from_patterns(user_data, market_patterns)
            variants.extend(pattern_variants)
        
        # Generate LLM variants if available
        if self.llm_client:
            llm_variants = await self._generate_with_llm(user_data, market_patterns)
            variants.extend(llm_variants)
        
        # Score and rank variants
        scored_variants = [self._score_headline(v, user_data) for v in variants]
        scored_variants.sort(key=lambda x: x.score, reverse=True)
        
        return scored_variants[:num_variants]
    
    def _generate_from_templates(self, user_data: Dict) -> List[str]:
        """Generate headlines from templates."""
        role = user_data.get("target_role", "Professional")
        role_type = self._categorize_role(role)
        
        template = self.templates.get(role_type, self.templates["default"])
        
        variants = []
        
        # Variant 1: Standard template
        headline1 = template.format(
            role=role,
            specialty=self._get_specialty(user_data),
            company_or_value=user_data.get("value_proposition", "Driving Impact"),
            outcome="Insights",
            industry=user_data.get("industry", "Technology"),
            achievement="Success",
            company_or_industry=user_data.get("industry", "Tech"),
            focus=user_data.get("focus_area", "User-Centered"),
            value_proposition=user_data.get("value_proposition", "Driving Results")
        )
        variants.append(headline1)
        
        # Variant 2: Skills-focused
        top_skills = user_data.get("top_skills", [])[:3]
        if top_skills:
            headline2 = f"{role} | {' • '.join(top_skills)}"
            variants.append(headline2)
        
        # Variant 3: Value-focused
        headline3 = f"{role} | Helping teams achieve {user_data.get('value_proposition', 'excellence')}"
        variants.append(headline3)
        
        return variants
    
    def _generate_from_patterns(
        self, user_data: Dict, patterns: Dict
    ) -> List[str]:
        """Generate headlines based on market patterns."""
        variants = []
        role = user_data.get("target_role", "Professional")
        
        # Use common formulas from patterns
        formulas = patterns.get("formulas", [])
        
        for formula in formulas[:2]:
            if formula.get("frequency", 0) > 20:
                # Apply high-frequency formulas
                if "Role + Value Prop" in formula.get("name", ""):
                    headline = f"{role} | {user_data.get('value_proposition', 'Driving Results')}"
                    variants.append(headline)
        
        # Use common keywords
        keywords = patterns.get("keywords", [])
        top_keywords = [k[0] for k in keywords[:3] if k[1] > 5]
        
        if top_keywords:
            keyword_headline = f"{role} | {' | '.join(top_keywords)}"
            variants.append(keyword_headline)
        
        return variants
    
    async def _generate_with_llm(
        self, user_data: Dict, patterns: Optional[Dict]
    ) -> List[str]:
        """Generate headlines using LLM."""
        prompt = self._build_llm_prompt(user_data, patterns)
        
        try:
            response = await self.llm_client.generate(prompt)
            
            # Parse LLM response into headlines
            lines = response.strip().split('\n')
            headlines = [line.strip().lstrip('0123456789.-) ') for line in lines if line.strip()]
            
            return headlines[:3]
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return []
    
    def _build_llm_prompt(self, user_data: Dict, patterns: Optional[Dict]) -> str:
        """Build prompt for LLM headline generation."""
        return f"""Generate 3 compelling LinkedIn headlines for:

Role: {user_data.get('target_role', 'Professional')}
Industry: {user_data.get('industry', 'Technology')}
Top Skills: {', '.join(user_data.get('top_skills', ['Leadership'])[:5])}
Value Proposition: {user_data.get('value_proposition', 'Driving results')}

Requirements:
- Maximum 150 characters each
- Include role and value proposition
- Use professional tone
- Make each variant unique

Return only the 3 headlines, one per line."""
    
    def _score_headline(self, headline: str, user_data: Dict) -> HeadlineResult:
        """Score a headline for quality."""
        score = 0
        patterns_used = []
        suggestions = []
        
        # Length scoring
        length = len(headline)
        if self.OPTIMAL_LENGTH[0] <= length <= self.OPTIMAL_LENGTH[1]:
            score += 25
            patterns_used.append("optimal_length")
        elif length > self.MAX_LENGTH:
            score -= 20
            suggestions.append("Headline exceeds maximum length")
        else:
            score += 10
        
        # Structure scoring
        if "|" in headline or "•" in headline:
            score += 15
            patterns_used.append("separator_used")
        
        # Role presence
        role = user_data.get("target_role", "").lower()
        if role and role in headline.lower():
            score += 20
            patterns_used.append("role_included")
        else:
            suggestions.append("Consider including your target role")
        
        # Value proposition
        value_words = ["helping", "driving", "building", "leading", "transforming"]
        if any(word in headline.lower() for word in value_words):
            score += 20
            patterns_used.append("value_proposition")
        else:
            suggestions.append("Add a value proposition")
        
        # Skill presence
        skills = user_data.get("top_skills", [])
        skill_match = sum(1 for s in skills if s.lower() in headline.lower())
        score += min(skill_match * 5, 15)
        if skill_match:
            patterns_used.append("skills_included")
        
        # Uniqueness (penalize generic phrases)
        generic_phrases = ["passionate about", "experienced in", "looking for"]
        if any(phrase in headline.lower() for phrase in generic_phrases):
            score -= 10
            suggestions.append("Avoid generic phrases")
        
        return HeadlineResult(
            headline=headline,
            score=max(0, min(score, 100)),
            patterns_used=patterns_used,
            character_count=length,
            suggestions=suggestions
        )
    
    def _categorize_role(self, role: str) -> str:
        """Categorize role for template selection."""
        role_lower = role.lower()
        
        if any(kw in role_lower for kw in ["developer", "engineer", "programmer"]):
            return "developer"
        elif any(kw in role_lower for kw in ["analyst", "scientist", "data"]):
            return "analyst"
        elif any(kw in role_lower for kw in ["manager", "director", "lead", "head"]):
            return "manager"
        elif any(kw in role_lower for kw in ["designer", "ux", "ui"]):
            return "designer"
        
        return "default"
    
    def _get_specialty(self, user_data: Dict) -> str:
        """Get specialty from user data."""
        skills = user_data.get("top_skills", [])
        if skills:
            return skills[0]
        return user_data.get("specialty", "Solutions")
