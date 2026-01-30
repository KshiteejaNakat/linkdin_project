"""
Portfolio Agent
Generates React-based portfolio with AI-driven content and layout decisions.
"""

from typing import Any, Dict, List
from loguru import logger

from .base_agent import BaseAgent, AgentAction


class PortfolioAgent(BaseAgent):
    """
    Agent responsible for generating personalized portfolios
    with intelligent layout and content decisions.
    """
    
    def __init__(self, llm_client: Any = None):
        super().__init__(
            name="PortfolioBuilder",
            description="Builds personalized React portfolios",
            llm_client=llm_client
        )
        self.layout_rules = self._load_layout_rules()
        
    def _load_layout_rules(self) -> Dict[str, Any]:
        """Load layout decision rules."""
        return {
            "developer": {
                "primary_sections": ["hero", "projects", "skills"],
                "layout_style": "project-first",
                "color_scheme": "tech-modern"
            },
            "analyst": {
                "primary_sections": ["hero", "metrics", "experience"],
                "layout_style": "metrics-first",
                "color_scheme": "professional"
            },
            "designer": {
                "primary_sections": ["hero", "portfolio", "about"],
                "layout_style": "visual-first",
                "color_scheme": "creative"
            },
            "manager": {
                "primary_sections": ["hero", "experience", "achievements"],
                "layout_style": "experience-first",
                "color_scheme": "executive"
            },
            "default": {
                "primary_sections": ["hero", "about", "skills", "experience"],
                "layout_style": "balanced",
                "color_scheme": "professional"
            }
        }
    
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decide portfolio generation strategy."""
        user_data = input_data.get("user_data", {})
        career_dna = input_data.get("career_dna", {})
        
        # Determine role category
        role_category = self._categorize_role(
            user_data.get("target_role", "")
        )
        
        # Get layout rules
        layout = self.layout_rules.get(role_category, self.layout_rules["default"])
        
        actions = [
            {
                "name": "generate_hero",
                "input": {"user_data": user_data, "style": layout["color_scheme"]}
            },
            {
                "name": "generate_sections",
                "input": {
                    "user_data": user_data,
                    "sections": layout["primary_sections"],
                    "career_dna": career_dna
                }
            },
            {
                "name": "generate_layout",
                "input": {
                    "layout_style": layout["layout_style"],
                    "color_scheme": layout["color_scheme"]
                }
            }
        ]
        
        return {
            "actions": actions,
            "strategy": "portfolio_generation",
            "role_category": role_category,
            "layout": layout
        }
    
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute portfolio generation actions."""
        action_map = {
            "generate_hero": self._generate_hero,
            "generate_sections": self._generate_sections,
            "generate_layout": self._generate_layout,
        }
        
        handler = action_map.get(action.name)
        if handler:
            return await handler(action.input_data)
        
        return {"error": f"Unknown action: {action.name}"}
    
    def _categorize_role(self, role: str) -> str:
        """Categorize role into portfolio layout category."""
        role_lower = role.lower()
        
        dev_keywords = ["developer", "engineer", "programmer", "architect"]
        analyst_keywords = ["analyst", "scientist", "researcher"]
        design_keywords = ["designer", "ux", "ui", "creative"]
        manager_keywords = ["manager", "director", "lead", "head", "vp"]
        
        if any(kw in role_lower for kw in dev_keywords):
            return "developer"
        elif any(kw in role_lower for kw in analyst_keywords):
            return "analyst"
        elif any(kw in role_lower for kw in design_keywords):
            return "designer"
        elif any(kw in role_lower for kw in manager_keywords):
            return "manager"
        return "default"
    
    async def _generate_hero(self, data: Dict) -> Dict[str, Any]:
        """Generate hero section content."""
        user_data = data.get("user_data", {})
        style = data.get("style", "professional")
        
        hero_content = {
            "name": user_data.get("name", ""),
            "title": user_data.get("target_role", ""),
            "tagline": self._generate_tagline(user_data),
            "cta_primary": "View My Work",
            "cta_secondary": "Contact Me",
            "style": style
        }
        
        return {"section": "hero", "content": hero_content}
    
    async def _generate_sections(self, data: Dict) -> Dict[str, Any]:
        """Generate all portfolio sections."""
        user_data = data.get("user_data", {})
        sections = data.get("sections", [])
        career_dna = data.get("career_dna", {})
        
        generated_sections = {}
        
        for section in sections:
            if section == "hero":
                continue  # Already handled
            elif section == "projects":
                generated_sections["projects"] = self._format_projects(user_data)
            elif section == "skills":
                generated_sections["skills"] = self._format_skills(user_data, career_dna)
            elif section == "experience":
                generated_sections["experience"] = self._format_experience(user_data)
            elif section == "about":
                generated_sections["about"] = self._format_about(user_data)
            elif section == "metrics":
                generated_sections["metrics"] = self._format_metrics(user_data, career_dna)
            elif section == "contact":
                generated_sections["contact"] = self._format_contact(user_data)
        
        return {"sections": generated_sections}
    
    async def _generate_layout(self, data: Dict) -> Dict[str, Any]:
        """Generate layout configuration."""
        layout_style = data.get("layout_style", "balanced")
        color_scheme = data.get("color_scheme", "professional")
        
        color_palettes = {
            "professional": {
                "primary": "#2563eb",
                "secondary": "#64748b",
                "background": "#ffffff",
                "text": "#1e293b"
            },
            "tech-modern": {
                "primary": "#8b5cf6",
                "secondary": "#06b6d4",
                "background": "#0f172a",
                "text": "#f1f5f9"
            },
            "creative": {
                "primary": "#ec4899",
                "secondary": "#f59e0b",
                "background": "#fdf4ff",
                "text": "#1e1b4b"
            },
            "executive": {
                "primary": "#0f172a",
                "secondary": "#475569",
                "background": "#f8fafc",
                "text": "#0f172a"
            }
        }
        
        return {
            "layout_style": layout_style,
            "colors": color_palettes.get(color_scheme, color_palettes["professional"]),
            "typography": self._get_typography(layout_style),
            "spacing": "comfortable"
        }
    
    def _generate_tagline(self, user_data: Dict) -> str:
        """Generate a compelling tagline."""
        role = user_data.get("target_role", "Professional")
        skills = user_data.get("top_skills", [])
        
        if skills:
            return f"Specializing in {skills[0]} | {role}"
        return f"Passionate {role} Building Impactful Solutions"
    
    def _format_projects(self, user_data: Dict) -> List[Dict]:
        """Format projects for portfolio display."""
        projects = user_data.get("projects", [])
        return [{
            "title": p.get("name", ""),
            "description": p.get("description", ""),
            "technologies": p.get("technologies", []),
            "link": p.get("url", ""),
            "image": p.get("image", "")
        } for p in projects]
    
    def _format_skills(self, user_data: Dict, career_dna: Dict) -> Dict:
        """Format skills with proficiency levels."""
        skills = user_data.get("skills", [])
        top_skills = career_dna.get("strengths", [])
        
        return {
            "highlighted": top_skills[:5],
            "all_skills": skills,
            "categories": self._categorize_skills(skills)
        }
    
    def _format_experience(self, user_data: Dict) -> List[Dict]:
        """Format experience timeline."""
        experience = user_data.get("experience", [])
        return [{
            "title": e.get("title", ""),
            "company": e.get("company", ""),
            "period": e.get("period", ""),
            "highlights": e.get("bullets", [])[:3]
        } for e in experience]
    
    def _format_about(self, user_data: Dict) -> Dict:
        """Format about section."""
        return {
            "summary": user_data.get("about", ""),
            "interests": user_data.get("interests", []),
            "values": user_data.get("values", [])
        }
    
    def _format_metrics(self, user_data: Dict, career_dna: Dict) -> List[Dict]:
        """Format key metrics for display."""
        return [
            {"label": "Years Experience", "value": user_data.get("years_exp", "5+")},
            {"label": "Projects Completed", "value": str(len(user_data.get("projects", [])))},
            {"label": "Skills", "value": str(len(user_data.get("skills", [])))}
        ]
    
    def _format_contact(self, user_data: Dict) -> Dict:
        """Format contact information."""
        return {
            "email": user_data.get("email", ""),
            "linkedin": user_data.get("linkedin_url", ""),
            "github": user_data.get("github_url", ""),
            "website": user_data.get("website", "")
        }
    
    def _categorize_skills(self, skills: List) -> Dict[str, List]:
        """Categorize skills for display."""
        categories = {"technical": [], "tools": [], "soft": []}
        for skill in skills:
            name = skill.get("name", skill) if isinstance(skill, dict) else skill
            categories["technical"].append(name)
        return categories
    
    def _get_typography(self, layout_style: str) -> Dict:
        """Get typography settings for layout style."""
        return {
            "heading_font": "Inter",
            "body_font": "Inter",
            "code_font": "Fira Code"
        }
