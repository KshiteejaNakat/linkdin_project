"""
Experience Optimizer Module
Optimizes LinkedIn experience section bullets.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class OptimizedExperience:
    """Optimized experience entry."""
    title: str
    company: str
    period: str
    bullets: List[str]
    score: int
    improvements: List[str]


class ExperienceOptimizer:
    """
    Optimizes LinkedIn experience section by transforming
    job descriptions into impactful, metric-driven bullets.
    """
    
    ACTION_VERBS = [
        "Led", "Developed", "Implemented", "Achieved", "Drove",
        "Designed", "Built", "Launched", "Increased", "Reduced",
        "Managed", "Created", "Established", "Spearheaded", "Orchestrated",
        "Delivered", "Transformed", "Optimized", "Streamlined", "Pioneered"
    ]
    
    def __init__(self, llm_client: Any = None):
        self.llm_client = llm_client
        
    async def optimize_all(
        self, experiences: List[Dict]
    ) -> List[OptimizedExperience]:
        """Optimize all experience entries."""
        optimized = []
        
        for exp in experiences:
            opt_exp = await self.optimize_experience(exp)
            optimized.append(opt_exp)
        
        return optimized
    
    async def optimize_experience(self, experience: Dict) -> OptimizedExperience:
        """Optimize a single experience entry."""
        title = experience.get("title", "")
        company = experience.get("company", "")
        period = experience.get("period", "")
        
        # Get original bullets or description
        original_bullets = experience.get("bullets", [])
        description = experience.get("description", "")
        
        if not original_bullets and description:
            original_bullets = self._extract_bullets(description)
        
        # Optimize bullets
        if self.llm_client:
            optimized_bullets = await self._optimize_with_llm(
                title, company, original_bullets
            )
        else:
            optimized_bullets = self._optimize_bullets(original_bullets)
        
        # Score and analyze
        score, improvements = self._score_experience(
            title, company, optimized_bullets
        )
        
        return OptimizedExperience(
            title=title,
            company=company,
            period=period,
            bullets=optimized_bullets,
            score=score,
            improvements=improvements
        )
    
    def _extract_bullets(self, description: str) -> List[str]:
        """Extract bullet points from description."""
        lines = description.split('\n')
        bullets = []
        
        for line in lines:
            cleaned = line.strip()
            if cleaned.startswith(('-', '•', '*', '→')):
                cleaned = cleaned[1:].strip()
            if cleaned and len(cleaned) > 10:
                bullets.append(cleaned)
        
        # If no bullets found, split by sentences
        if not bullets:
            sentences = description.replace('...', '.').split('.')
            bullets = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        return bullets[:6]
    
    def _optimize_bullets(self, bullets: List[str]) -> List[str]:
        """Optimize bullets using template-based approach."""
        optimized = []
        
        for bullet in bullets:
            optimized_bullet = self._transform_bullet(bullet)
            optimized.append(optimized_bullet)
        
        return optimized[:5]  # Limit to 5 bullets
    
    def _transform_bullet(self, bullet: str) -> str:
        """Transform a single bullet to be more impactful."""
        words = bullet.split()
        
        if not words:
            return bullet
        
        # Check if already starts with action verb
        first_word = words[0].strip(',-.')
        if first_word in self.ACTION_VERBS:
            return bullet
        
        # Detect responsibility type and add appropriate verb
        bullet_lower = bullet.lower()
        
        if any(kw in bullet_lower for kw in ["team", "people", "staff"]):
            return f"Led {bullet[0].lower()}{bullet[1:]}"
        elif any(kw in bullet_lower for kw in ["built", "created", "made"]):
            return f"Developed {bullet[0].lower()}{bullet[1:]}"
        elif any(kw in bullet_lower for kw in ["improved", "increased", "grew"]):
            return f"Drove {bullet[0].lower()}{bullet[1:]}"
        elif any(kw in bullet_lower for kw in ["responsible", "handled", "managed"]):
            return f"Managed {self._remove_weak_start(bullet)}"
        else:
            return f"Delivered {bullet[0].lower()}{bullet[1:]}"
    
    def _remove_weak_start(self, text: str) -> str:
        """Remove weak starting phrases."""
        weak_phrases = [
            "responsible for", "handled", "worked on",
            "assisted with", "helped with", "was involved in"
        ]
        
        text_lower = text.lower()
        for phrase in weak_phrases:
            if text_lower.startswith(phrase):
                return text[len(phrase):].strip()
        
        return text
    
    async def _optimize_with_llm(
        self, title: str, company: str, bullets: List[str]
    ) -> List[str]:
        """Optimize bullets using LLM."""
        if not bullets:
            return []
        
        prompt = f"""Transform these job responsibilities into impactful, metric-driven bullet points:

Role: {title} at {company}

Original bullets:
{chr(10).join(['- ' + b for b in bullets])}

Requirements:
- Start each bullet with a strong action verb
- Include quantifiable results where possible
- Be specific and concise (max 150 characters each)
- Focus on impact and achievements
- Use professional language

Return only the optimized bullets, one per line, starting with '-':"""
        
        try:
            response = await self.llm_client.generate(prompt)
            
            # Parse response
            lines = response.strip().split('\n')
            optimized = []
            for line in lines:
                cleaned = line.strip().lstrip('-•* ')
                if cleaned and len(cleaned) > 10:
                    optimized.append(cleaned)
            
            return optimized[:5]
        except Exception as e:
            logger.error(f"LLM optimization error: {e}")
            return self._optimize_bullets(bullets)
    
    def _score_experience(
        self, title: str, company: str, bullets: List[str]
    ) -> tuple:
        """Score experience quality and identify improvements."""
        score = 0
        improvements = []
        
        # Bullet count scoring
        bullet_count = len(bullets)
        if 3 <= bullet_count <= 5:
            score += 25
        elif bullet_count < 3:
            improvements.append("Add more bullet points (aim for 3-5)")
            score += 10
        else:
            score += 20
        
        # Action verb scoring
        action_verb_count = 0
        for bullet in bullets:
            first_word = bullet.split()[0] if bullet.split() else ""
            if first_word in self.ACTION_VERBS:
                action_verb_count += 1
        
        if action_verb_count == len(bullets) and bullets:
            score += 25
        elif action_verb_count > 0:
            score += 15
            improvements.append("Start all bullets with action verbs")
        else:
            improvements.append("Start bullets with action verbs")
        
        # Metrics scoring
        metrics_count = 0
        for bullet in bullets:
            if any(char.isdigit() for char in bullet):
                metrics_count += 1
        
        if metrics_count >= len(bullets) // 2:
            score += 25
        elif metrics_count > 0:
            score += 15
        else:
            improvements.append("Add quantifiable metrics (%, $, numbers)")
        
        # Length scoring
        good_length_count = sum(
            1 for b in bullets if 50 <= len(b) <= 150
        )
        if good_length_count == len(bullets) and bullets:
            score += 15
        elif good_length_count > 0:
            score += 10
        
        # Keywords scoring
        impact_words = ["achieved", "improved", "increased", "reduced", "delivered"]
        has_impact = any(
            any(w in b.lower() for w in impact_words) for b in bullets
        )
        if has_impact:
            score += 10
        else:
            improvements.append("Highlight impact and achievements")
        
        return min(score, 100), improvements
    
    def generate_bullets_from_role(
        self, role: str, industry: str, level: str = "mid"
    ) -> List[str]:
        """Generate sample bullets for a role."""
        role_templates = {
            "software engineer": [
                "Developed scalable microservices handling 1M+ daily requests",
                "Led implementation of CI/CD pipeline, reducing deployment time by 60%",
                "Mentored 3 junior developers, improving team velocity by 25%",
                "Architected cloud-native solutions on AWS, reducing costs by 40%"
            ],
            "data scientist": [
                "Built ML models achieving 92% prediction accuracy",
                "Automated data pipeline processing 5TB+ daily",
                "Delivered insights driving $2M+ in revenue optimization",
                "Created dashboards used by 50+ stakeholders for decision-making"
            ],
            "product manager": [
                "Launched 3 products generating $5M+ ARR",
                "Increased user engagement by 45% through feature optimization",
                "Led cross-functional team of 12 across 4 time zones",
                "Defined product roadmap aligned with company OKRs"
            ]
        }
        
        role_lower = role.lower()
        for key, bullets in role_templates.items():
            if key in role_lower:
                return bullets
        
        return [
            f"Led key initiatives at the organization",
            f"Collaborated with cross-functional teams to deliver results",
            f"Implemented improvements that enhanced efficiency"
        ]
