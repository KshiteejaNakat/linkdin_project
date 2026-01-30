"""
Content Generator Agent
Generates optimized content for LinkedIn profiles using LLM.
"""

from typing import Any, Dict, List
from loguru import logger

from .base_agent import BaseAgent, AgentAction


class ContentGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating optimized profile content
    using LLM and market intelligence.
    """
    
    def __init__(self, llm_client: Any = None):
        super().__init__(
            name="ContentGenerator",
            description="Generates optimized profile content",
            llm_client=llm_client
        )
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """Load content generation templates."""
        return {
            "headline": """Generate a compelling LinkedIn headline for:
Role: {role}
Industry: {industry}
Key Skills: {skills}
Value Proposition: {value_prop}

Requirements:
- Maximum 120 characters
- Include role and value proposition
- Use power words
- Make it specific and impactful""",

            "about": """Write a professional LinkedIn About section for:
Name: {name}
Current Role: {role}
Industry: {industry}
Experience Summary: {experience}
Key Achievements: {achievements}
Career Goals: {goals}

Requirements:
- 200-300 words
- First person perspective
- Hook in first line
- Include achievements with metrics
- End with call-to-action""",

            "experience_bullet": """Transform this experience into impactful bullet points:
Role: {role}
Company: {company}
Responsibilities: {responsibilities}

Requirements:
- Start with action verb
- Include quantifiable results
- Be specific and concise
- 3-5 bullet points"""
        }
    
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decide what content to generate."""
        content_type = input_data.get("content_type", "all")
        user_data = input_data.get("user_data", {})
        market_patterns = input_data.get("market_patterns", {})
        
        actions = []
        
        if content_type in ["all", "headline"]:
            actions.append({
                "name": "generate_headline",
                "input": {
                    "user_data": user_data,
                    "patterns": market_patterns.get("headline", {})
                }
            })
            
        if content_type in ["all", "about"]:
            actions.append({
                "name": "generate_about",
                "input": {
                    "user_data": user_data,
                    "patterns": market_patterns.get("about", {})
                }
            })
            
        if content_type in ["all", "experience"]:
            actions.append({
                "name": "generate_experience",
                "input": {
                    "user_data": user_data,
                    "patterns": market_patterns.get("experience", {})
                }
            })
        
        return {"actions": actions, "strategy": "content_generation"}
    
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute content generation actions."""
        action_map = {
            "generate_headline": self._generate_headline,
            "generate_about": self._generate_about,
            "generate_experience": self._generate_experience,
        }
        
        handler = action_map.get(action.name)
        if handler:
            return await handler(action.input_data)
        
        return {"error": f"Unknown action: {action.name}"}
    
    async def _generate_headline(self, data: Dict) -> Dict[str, Any]:
        """Generate optimized headline."""
        user_data = data.get("user_data", {})
        
        prompt = self.templates["headline"].format(
            role=user_data.get("target_role", "Professional"),
            industry=user_data.get("industry", "Technology"),
            skills=", ".join(user_data.get("top_skills", ["Leadership"])),
            value_prop=user_data.get("value_proposition", "Driving results")
        )
        
        if self.llm_client:
            generated = await self.llm_client.generate(prompt)
        else:
            # Fallback template-based generation
            generated = self._template_headline(user_data)
        
        return {
            "section": "headline",
            "content": generated,
            "prompt_used": prompt
        }
    
    async def _generate_about(self, data: Dict) -> Dict[str, Any]:
        """Generate optimized about section."""
        user_data = data.get("user_data", {})
        
        prompt = self.templates["about"].format(
            name=user_data.get("name", "Professional"),
            role=user_data.get("current_role", ""),
            industry=user_data.get("industry", ""),
            experience=user_data.get("experience_summary", ""),
            achievements=", ".join(user_data.get("achievements", [])),
            goals=user_data.get("career_goals", "")
        )
        
        if self.llm_client:
            generated = await self.llm_client.generate(prompt)
        else:
            generated = self._template_about(user_data)
        
        return {
            "section": "about",
            "content": generated,
            "prompt_used": prompt
        }
    
    async def _generate_experience(self, data: Dict) -> Dict[str, Any]:
        """Generate optimized experience bullets."""
        user_data = data.get("user_data", {})
        experiences = user_data.get("experience", [])
        
        optimized_experiences = []
        for exp in experiences:
            prompt = self.templates["experience_bullet"].format(
                role=exp.get("title", ""),
                company=exp.get("company", ""),
                responsibilities=exp.get("description", "")
            )
            
            if self.llm_client:
                bullets = await self.llm_client.generate(prompt)
            else:
                bullets = self._template_experience(exp)
            
            optimized_experiences.append({
                "title": exp.get("title"),
                "company": exp.get("company"),
                "bullets": bullets
            })
        
        return {
            "section": "experience",
            "content": optimized_experiences
        }
    
    def _template_headline(self, user_data: Dict) -> str:
        """Fallback headline template."""
        role = user_data.get("target_role", "Professional")
        industry = user_data.get("industry", "")
        skills = user_data.get("top_skills", [])
        
        skill_str = " & ".join(skills[:2]) if skills else "Excellence"
        return f"{role} | {skill_str} | Driving Impact in {industry}"
    
    def _template_about(self, user_data: Dict) -> str:
        """Fallback about template."""
        name = user_data.get("name", "I")
        role = user_data.get("current_role", "professional")
        industry = user_data.get("industry", "my field")
        
        return f"""Passionate {role} with expertise in {industry}.

I thrive on solving complex challenges and delivering measurable results. 
My approach combines strategic thinking with hands-on execution.

Key areas of expertise:
• {user_data.get('top_skills', ['Leadership', 'Innovation'])[0]}
• Strategic Planning
• Team Collaboration

Let's connect to explore how we can create value together.
📧 Feel free to reach out!"""
    
    def _template_experience(self, exp: Dict) -> List[str]:
        """Fallback experience bullets."""
        return [
            f"Led initiatives at {exp.get('company', 'the organization')}",
            "Collaborated with cross-functional teams to deliver results",
            "Implemented improvements that enhanced efficiency",
        ]
