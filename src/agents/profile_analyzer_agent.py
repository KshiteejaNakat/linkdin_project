"""
Profile Analyzer Agent
Analyzes LinkedIn profiles and extracts patterns from top performers.
"""

from typing import Any, Dict, List, Optional
from loguru import logger

from .base_agent import BaseAgent, AgentAction, AgentMessage


class ProfileAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing top-performing profiles
    and extracting success patterns.
    """
    
    def __init__(self, llm_client: Any = None):
        super().__init__(
            name="ProfileAnalyzer",
            description="Analyzes profiles to extract success patterns",
            llm_client=llm_client
        )
        self.analysis_cache: Dict[str, Any] = {}
        
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide what analysis actions to perform.
        """
        profile_data = input_data.get("profile_data", {})
        analysis_type = input_data.get("analysis_type", "full")
        
        actions = []
        
        if analysis_type in ["full", "headline"]:
            actions.append({
                "name": "analyze_headline",
                "input": {"headline": profile_data.get("headline", "")}
            })
            
        if analysis_type in ["full", "about"]:
            actions.append({
                "name": "analyze_about",
                "input": {"about": profile_data.get("about", "")}
            })
            
        if analysis_type in ["full", "experience"]:
            actions.append({
                "name": "analyze_experience",
                "input": {"experience": profile_data.get("experience", [])}
            })
            
        if analysis_type in ["full", "skills"]:
            actions.append({
                "name": "analyze_skills",
                "input": {"skills": profile_data.get("skills", [])}
            })
        
        return {"actions": actions, "strategy": "comprehensive_analysis"}
    
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute profile analysis actions."""
        
        action_map = {
            "analyze_headline": self._analyze_headline,
            "analyze_about": self._analyze_about,
            "analyze_experience": self._analyze_experience,
            "analyze_skills": self._analyze_skills,
        }
        
        handler = action_map.get(action.name)
        if handler:
            return await handler(action.input_data)
        
        return {"error": f"Unknown action: {action.name}"}
    
    async def _analyze_headline(self, data: Dict) -> Dict[str, Any]:
        """Analyze headline patterns."""
        headline = data.get("headline", "")
        
        patterns = {
            "has_title": bool(headline),
            "word_count": len(headline.split()) if headline else 0,
            "has_value_proposition": any(
                kw in headline.lower() 
                for kw in ["helping", "driving", "building", "leading"]
            ),
            "has_metrics": any(char.isdigit() for char in headline),
            "uses_separator": "|" in headline or "•" in headline,
        }
        
        score = sum([
            patterns["has_title"] * 20,
            min(patterns["word_count"] * 5, 25),
            patterns["has_value_proposition"] * 25,
            patterns["has_metrics"] * 15,
            patterns["uses_separator"] * 15,
        ])
        
        return {
            "section": "headline",
            "patterns": patterns,
            "score": min(score, 100),
            "recommendations": self._get_headline_recommendations(patterns)
        }
    
    async def _analyze_about(self, data: Dict) -> Dict[str, Any]:
        """Analyze about section patterns."""
        about = data.get("about", "")
        
        patterns = {
            "has_content": bool(about),
            "word_count": len(about.split()) if about else 0,
            "has_call_to_action": any(
                kw in about.lower() 
                for kw in ["reach out", "connect", "contact", "email"]
            ),
            "has_achievements": any(
                kw in about.lower() 
                for kw in ["achieved", "increased", "reduced", "led"]
            ),
            "uses_first_person": about.lower().startswith("i ") if about else False,
        }
        
        return {
            "section": "about",
            "patterns": patterns,
            "score": self._calculate_about_score(patterns),
            "recommendations": self._get_about_recommendations(patterns)
        }
    
    async def _analyze_experience(self, data: Dict) -> Dict[str, Any]:
        """Analyze experience section patterns."""
        experience = data.get("experience", [])
        
        patterns = {
            "total_positions": len(experience),
            "has_descriptions": sum(1 for e in experience if e.get("description")),
            "avg_bullets": self._calculate_avg_bullets(experience),
            "has_metrics": self._check_experience_metrics(experience),
        }
        
        return {
            "section": "experience",
            "patterns": patterns,
            "score": self._calculate_experience_score(patterns),
            "recommendations": self._get_experience_recommendations(patterns)
        }
    
    async def _analyze_skills(self, data: Dict) -> Dict[str, Any]:
        """Analyze skills section patterns."""
        skills = data.get("skills", [])
        
        patterns = {
            "total_skills": len(skills),
            "has_endorsements": sum(1 for s in skills if s.get("endorsements", 0) > 0),
            "skill_categories": self._categorize_skills(skills),
        }
        
        return {
            "section": "skills",
            "patterns": patterns,
            "score": self._calculate_skills_score(patterns),
            "recommendations": self._get_skills_recommendations(patterns)
        }
    
    def _calculate_avg_bullets(self, experience: List) -> float:
        """Calculate average bullet points per experience."""
        if not experience:
            return 0
        bullets = [len(e.get("bullets", [])) for e in experience]
        return sum(bullets) / len(bullets) if bullets else 0
    
    def _check_experience_metrics(self, experience: List) -> int:
        """Count experiences with quantifiable metrics."""
        count = 0
        for exp in experience:
            desc = exp.get("description", "")
            if any(char.isdigit() for char in desc):
                count += 1
        return count
    
    def _categorize_skills(self, skills: List) -> Dict[str, int]:
        """Categorize skills into groups."""
        categories = {"technical": 0, "soft": 0, "tools": 0, "other": 0}
        # Simplified categorization
        for skill in skills:
            name = skill.get("name", "").lower() if isinstance(skill, dict) else skill.lower()
            if any(kw in name for kw in ["python", "java", "sql", "aws"]):
                categories["technical"] += 1
            elif any(kw in name for kw in ["leadership", "communication"]):
                categories["soft"] += 1
            else:
                categories["other"] += 1
        return categories
    
    def _calculate_about_score(self, patterns: Dict) -> int:
        return min(sum([
            patterns["has_content"] * 30,
            min(patterns["word_count"] // 10, 30),
            patterns["has_call_to_action"] * 20,
            patterns["has_achievements"] * 20,
        ]), 100)
    
    def _calculate_experience_score(self, patterns: Dict) -> int:
        return min(sum([
            min(patterns["total_positions"] * 15, 30),
            patterns["has_descriptions"] * 10,
            min(int(patterns["avg_bullets"] * 10), 20),
            patterns["has_metrics"] * 10,
        ]), 100)
    
    def _calculate_skills_score(self, patterns: Dict) -> int:
        return min(sum([
            min(patterns["total_skills"] * 3, 40),
            min(patterns["has_endorsements"] * 5, 30),
            30 if patterns["skill_categories"]["technical"] > 5 else 15,
        ]), 100)
    
    def _get_headline_recommendations(self, patterns: Dict) -> List[str]:
        recs = []
        if not patterns["has_value_proposition"]:
            recs.append("Add a value proposition to your headline")
        if not patterns["has_metrics"]:
            recs.append("Include quantifiable achievements")
        return recs
    
    def _get_about_recommendations(self, patterns: Dict) -> List[str]:
        recs = []
        if patterns["word_count"] < 100:
            recs.append("Expand your about section (aim for 200+ words)")
        if not patterns["has_call_to_action"]:
            recs.append("Add a call-to-action at the end")
        return recs
    
    def _get_experience_recommendations(self, patterns: Dict) -> List[str]:
        recs = []
        if patterns["avg_bullets"] < 3:
            recs.append("Add more bullet points to each experience")
        if patterns["has_metrics"] < patterns["total_positions"] // 2:
            recs.append("Include more quantifiable metrics")
        return recs
    
    def _get_skills_recommendations(self, patterns: Dict) -> List[str]:
        recs = []
        if patterns["total_skills"] < 10:
            recs.append("Add more relevant skills (aim for 15-20)")
        return recs
