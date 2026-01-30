"""
Market Analyzer Module
Analyzes market trends and skill demands for career optimization.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger


@dataclass
class MarketTrend:
    """Represents a market trend."""
    name: str
    category: str
    growth_rate: float  # Percentage growth
    demand_score: int  # 1-100
    time_period: str
    sources: List[str] = field(default_factory=list)


@dataclass
class SkillDemand:
    """Represents skill demand in the market."""
    skill_name: str
    demand_score: int
    trending: bool
    related_roles: List[str]
    salary_impact: float  # Percentage salary boost


class MarketAnalyzer:
    """
    Analyzes job market trends to inform profile optimization.
    """
    
    def __init__(self):
        self.trend_cache: Dict[str, List[MarketTrend]] = {}
        self.skill_demand_cache: Dict[str, SkillDemand] = {}
        self._last_update: Optional[datetime] = None
        
    async def analyze_industry_trends(
        self, industry: str
    ) -> Dict[str, Any]:
        """Analyze trends for a specific industry."""
        logger.info(f"Analyzing trends for: {industry}")
        
        trends = self._get_industry_trends(industry)
        
        return {
            "industry": industry,
            "trends": trends,
            "emerging_skills": self._get_emerging_skills(industry),
            "declining_skills": self._get_declining_skills(industry),
            "market_outlook": self._get_market_outlook(industry)
        }
    
    async def get_skill_demand(
        self, skills: List[str], industry: str
    ) -> Dict[str, SkillDemand]:
        """Get demand scores for specific skills."""
        demand_data = {}
        
        for skill in skills:
            demand_data[skill] = self._calculate_skill_demand(skill, industry)
        
        return demand_data
    
    async def get_role_requirements(
        self, role: str, industry: str
    ) -> Dict[str, Any]:
        """Get typical requirements for a role."""
        return {
            "role": role,
            "industry": industry,
            "required_skills": self._get_role_skills(role, "required"),
            "preferred_skills": self._get_role_skills(role, "preferred"),
            "experience_range": self._get_experience_range(role),
            "certifications": self._get_recommended_certs(role, industry)
        }
    
    def compare_with_market(
        self, user_skills: List[str], target_role: str, industry: str
    ) -> Dict[str, Any]:
        """Compare user skills with market requirements."""
        role_skills = self._get_role_skills(target_role, "all")
        
        user_skill_set = set(s.lower() for s in user_skills)
        role_skill_set = set(s.lower() for s in role_skills)
        
        matching = user_skill_set.intersection(role_skill_set)
        missing = role_skill_set - user_skill_set
        extra = user_skill_set - role_skill_set
        
        return {
            "match_percentage": len(matching) / len(role_skill_set) * 100 if role_skill_set else 0,
            "matching_skills": list(matching),
            "missing_skills": list(missing),
            "additional_skills": list(extra),
            "recommendations": self._generate_skill_recommendations(missing)
        }
    
    def _get_industry_trends(self, industry: str) -> List[Dict]:
        """Get trends for an industry."""
        # Industry-specific trend data
        trends_db = {
            "technology": [
                {"name": "AI/ML Integration", "growth": 45, "impact": "high"},
                {"name": "Cloud-Native Development", "growth": 35, "impact": "high"},
                {"name": "DevSecOps", "growth": 30, "impact": "medium"},
                {"name": "Remote-First Teams", "growth": 25, "impact": "medium"}
            ],
            "finance": [
                {"name": "FinTech Innovation", "growth": 40, "impact": "high"},
                {"name": "Regulatory Technology", "growth": 30, "impact": "medium"},
                {"name": "ESG Investing", "growth": 35, "impact": "high"}
            ],
            "healthcare": [
                {"name": "Telehealth", "growth": 50, "impact": "high"},
                {"name": "AI Diagnostics", "growth": 40, "impact": "high"},
                {"name": "Digital Health Records", "growth": 25, "impact": "medium"}
            ]
        }
        
        return trends_db.get(industry.lower(), [
            {"name": "Digital Transformation", "growth": 30, "impact": "high"},
            {"name": "Data-Driven Decision Making", "growth": 25, "impact": "medium"}
        ])
    
    def _get_emerging_skills(self, industry: str) -> List[Dict]:
        """Get emerging skills for an industry."""
        emerging_db = {
            "technology": [
                {"skill": "LLM/GenAI", "demand_growth": 150},
                {"skill": "Kubernetes", "demand_growth": 45},
                {"skill": "Rust", "demand_growth": 40},
                {"skill": "Platform Engineering", "demand_growth": 55}
            ],
            "finance": [
                {"skill": "Python for Finance", "demand_growth": 60},
                {"skill": "Blockchain", "demand_growth": 35},
                {"skill": "Risk Modeling", "demand_growth": 30}
            ],
            "default": [
                {"skill": "Data Analysis", "demand_growth": 40},
                {"skill": "Project Management", "demand_growth": 25}
            ]
        }
        
        return emerging_db.get(industry.lower(), emerging_db["default"])
    
    def _get_declining_skills(self, industry: str) -> List[Dict]:
        """Get declining skills for an industry."""
        return [
            {"skill": "Legacy Systems Maintenance", "decline_rate": 20},
            {"skill": "Manual Testing", "decline_rate": 15}
        ]
    
    def _get_market_outlook(self, industry: str) -> Dict[str, Any]:
        """Get overall market outlook."""
        return {
            "growth_forecast": "positive",
            "hiring_trend": "increasing",
            "salary_trend": "stable_to_increasing",
            "remote_opportunities": "high"
        }
    
    def _calculate_skill_demand(self, skill: str, industry: str) -> SkillDemand:
        """Calculate demand for a specific skill."""
        # Simplified demand calculation
        high_demand_skills = {
            "python": 95, "aws": 90, "kubernetes": 85,
            "machine learning": 92, "data science": 88,
            "react": 82, "typescript": 80
        }
        
        demand_score = high_demand_skills.get(skill.lower(), 50)
        
        return SkillDemand(
            skill_name=skill,
            demand_score=demand_score,
            trending=demand_score > 75,
            related_roles=self._get_related_roles(skill),
            salary_impact=self._estimate_salary_impact(demand_score)
        )
    
    def _get_role_skills(self, role: str, skill_type: str) -> List[str]:
        """Get skills for a specific role."""
        role_skills = {
            "software engineer": {
                "required": ["Python", "Git", "SQL", "Problem Solving"],
                "preferred": ["AWS", "Docker", "Kubernetes", "CI/CD"]
            },
            "data scientist": {
                "required": ["Python", "SQL", "Statistics", "Machine Learning"],
                "preferred": ["TensorFlow", "PyTorch", "Spark", "Tableau"]
            },
            "product manager": {
                "required": ["Product Strategy", "Roadmapping", "User Research"],
                "preferred": ["SQL", "A/B Testing", "Agile", "Data Analysis"]
            }
        }
        
        role_lower = role.lower()
        skills = role_skills.get(role_lower, {
            "required": ["Communication", "Problem Solving"],
            "preferred": ["Leadership", "Data Analysis"]
        })
        
        if skill_type == "all":
            return skills["required"] + skills["preferred"]
        return skills.get(skill_type, [])
    
    def _get_experience_range(self, role: str) -> Dict[str, int]:
        """Get typical experience range for a role."""
        experience_map = {
            "junior": {"min": 0, "max": 2},
            "mid": {"min": 2, "max": 5},
            "senior": {"min": 5, "max": 10},
            "lead": {"min": 7, "max": 15}
        }
        
        role_lower = role.lower()
        if "senior" in role_lower or "sr" in role_lower:
            return experience_map["senior"]
        elif "lead" in role_lower or "principal" in role_lower:
            return experience_map["lead"]
        elif "junior" in role_lower or "jr" in role_lower:
            return experience_map["junior"]
        return experience_map["mid"]
    
    def _get_recommended_certs(self, role: str, industry: str) -> List[str]:
        """Get recommended certifications."""
        cert_map = {
            "technology": ["AWS Solutions Architect", "GCP Professional", "PMP"],
            "data": ["Google Data Analytics", "AWS Data Analytics"],
            "security": ["CISSP", "CEH", "Security+"]
        }
        
        return cert_map.get(industry.lower(), ["Industry Certification"])
    
    def _get_related_roles(self, skill: str) -> List[str]:
        """Get roles related to a skill."""
        skill_role_map = {
            "python": ["Software Engineer", "Data Scientist", "ML Engineer"],
            "aws": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
            "machine learning": ["ML Engineer", "Data Scientist", "AI Researcher"]
        }
        
        return skill_role_map.get(skill.lower(), ["Various Technical Roles"])
    
    def _estimate_salary_impact(self, demand_score: int) -> float:
        """Estimate salary impact based on demand."""
        if demand_score >= 90:
            return 15.0
        elif demand_score >= 80:
            return 10.0
        elif demand_score >= 70:
            return 5.0
        return 0.0
    
    def _generate_skill_recommendations(self, missing_skills: set) -> List[Dict]:
        """Generate recommendations for missing skills."""
        recommendations = []
        
        for skill in list(missing_skills)[:5]:
            recommendations.append({
                "skill": skill,
                "priority": "high" if skill in {"Python", "AWS", "SQL"} else "medium",
                "learning_resources": [
                    f"Online courses for {skill}",
                    f"Hands-on projects with {skill}"
                ]
            })
        
        return recommendations
