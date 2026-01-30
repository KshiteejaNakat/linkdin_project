"""
Layout Selector Module
Selects optimal portfolio layout based on role and content.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LayoutStyle(Enum):
    """Portfolio layout styles."""
    MINIMAL = "minimal"
    MODERN = "modern"
    CREATIVE = "creative"
    PROFESSIONAL = "professional"
    DEVELOPER = "developer"


@dataclass
class ColorScheme:
    """Portfolio color scheme."""
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str


@dataclass
class LayoutConfig:
    """Complete layout configuration."""
    style: LayoutStyle
    sections: List[str]
    colors: ColorScheme
    typography: Dict[str, str]
    spacing: str
    animations: bool = True


class LayoutSelector:
    """
    Selects optimal portfolio layout based on
    user role, industry, and content analysis.
    """
    
    def __init__(self):
        self.color_schemes = self._load_color_schemes()
        self.section_orders = self._load_section_orders()
        
    def _load_color_schemes(self) -> Dict[str, ColorScheme]:
        """Load predefined color schemes."""
        return {
            "professional": ColorScheme(
                primary="#2563eb",
                secondary="#64748b",
                accent="#0ea5e9",
                background="#ffffff",
                surface="#f8fafc",
                text_primary="#0f172a",
                text_secondary="#475569"
            ),
            "dark_tech": ColorScheme(
                primary="#8b5cf6",
                secondary="#06b6d4",
                accent="#f59e0b",
                background="#0f172a",
                surface="#1e293b",
                text_primary="#f1f5f9",
                text_secondary="#94a3b8"
            ),
            "creative": ColorScheme(
                primary="#ec4899",
                secondary="#8b5cf6",
                accent="#06b6d4",
                background="#fdf4ff",
                surface="#ffffff",
                text_primary="#1e1b4b",
                text_secondary="#6b7280"
            ),
            "minimal": ColorScheme(
                primary="#000000",
                secondary="#6b7280",
                accent="#2563eb",
                background="#ffffff",
                surface="#f9fafb",
                text_primary="#111827",
                text_secondary="#6b7280"
            ),
            "nature": ColorScheme(
                primary="#059669",
                secondary="#0d9488",
                accent="#84cc16",
                background="#f0fdf4",
                surface="#ffffff",
                text_primary="#064e3b",
                text_secondary="#475569"
            )
        }
    
    def _load_section_orders(self) -> Dict[str, List[str]]:
        """Load section orders by role type."""
        return {
            "developer": [
                "hero", "about", "skills", "projects", 
                "experience", "education", "contact"
            ],
            "designer": [
                "hero", "portfolio", "about", "skills",
                "experience", "contact"
            ],
            "analyst": [
                "hero", "about", "metrics", "skills",
                "experience", "projects", "education", "contact"
            ],
            "manager": [
                "hero", "about", "experience", "achievements",
                "skills", "education", "contact"
            ],
            "default": [
                "hero", "about", "skills", "experience",
                "projects", "education", "contact"
            ]
        }
    
    def select_layout(
        self,
        role: str,
        industry: str,
        content_analysis: Optional[Dict] = None,
        preferences: Optional[Dict] = None
    ) -> LayoutConfig:
        """Select optimal layout configuration."""
        
        # Determine style based on role/industry
        style = self._determine_style(role, industry)
        
        # Get section order
        role_type = self._categorize_role(role)
        sections = self.section_orders.get(role_type, self.section_orders["default"])
        
        # Adjust sections based on content
        if content_analysis:
            sections = self._adjust_sections(sections, content_analysis)
        
        # Select color scheme
        color_scheme = self._select_colors(style, industry, preferences)
        
        # Get typography
        typography = self._select_typography(style)
        
        return LayoutConfig(
            style=style,
            sections=sections,
            colors=color_scheme,
            typography=typography,
            spacing="comfortable",
            animations=True
        )
    
    def _determine_style(self, role: str, industry: str) -> LayoutStyle:
        """Determine layout style based on role and industry."""
        role_lower = role.lower()
        industry_lower = industry.lower()
        
        # Developer-specific
        if any(kw in role_lower for kw in ["developer", "engineer", "programmer"]):
            return LayoutStyle.DEVELOPER
        
        # Creative roles
        if any(kw in role_lower for kw in ["designer", "creative", "artist"]):
            return LayoutStyle.CREATIVE
        
        # Industry-based
        if industry_lower in ["finance", "consulting", "legal"]:
            return LayoutStyle.PROFESSIONAL
        elif industry_lower in ["tech", "startup", "technology"]:
            return LayoutStyle.MODERN
        
        return LayoutStyle.MODERN
    
    def _categorize_role(self, role: str) -> str:
        """Categorize role for section ordering."""
        role_lower = role.lower()
        
        if any(kw in role_lower for kw in ["developer", "engineer", "programmer"]):
            return "developer"
        elif any(kw in role_lower for kw in ["designer", "ux", "ui"]):
            return "designer"
        elif any(kw in role_lower for kw in ["analyst", "scientist", "data"]):
            return "analyst"
        elif any(kw in role_lower for kw in ["manager", "director", "lead"]):
            return "manager"
        
        return "default"
    
    def _adjust_sections(
        self, sections: List[str], content_analysis: Dict
    ) -> List[str]:
        """Adjust sections based on available content."""
        adjusted = sections.copy()
        
        # Remove sections without content
        if not content_analysis.get("has_projects"):
            adjusted = [s for s in adjusted if s != "projects"]
        
        if not content_analysis.get("has_education"):
            adjusted = [s for s in adjusted if s != "education"]
        
        # Add testimonials if available
        if content_analysis.get("has_testimonials"):
            # Insert before contact
            if "contact" in adjusted:
                idx = adjusted.index("contact")
                adjusted.insert(idx, "testimonials")
        
        return adjusted
    
    def _select_colors(
        self,
        style: LayoutStyle,
        industry: str,
        preferences: Optional[Dict]
    ) -> ColorScheme:
        """Select color scheme."""
        # Check user preferences first
        if preferences and preferences.get("color_scheme"):
            scheme_name = preferences["color_scheme"]
            if scheme_name in self.color_schemes:
                return self.color_schemes[scheme_name]
        
        # Style-based selection
        style_color_map = {
            LayoutStyle.DEVELOPER: "dark_tech",
            LayoutStyle.CREATIVE: "creative",
            LayoutStyle.PROFESSIONAL: "professional",
            LayoutStyle.MINIMAL: "minimal",
            LayoutStyle.MODERN: "professional"
        }
        
        scheme_name = style_color_map.get(style, "professional")
        return self.color_schemes[scheme_name]
    
    def _select_typography(self, style: LayoutStyle) -> Dict[str, str]:
        """Select typography based on style."""
        typography_options = {
            LayoutStyle.DEVELOPER: {
                "heading": "JetBrains Mono",
                "body": "Inter",
                "code": "Fira Code"
            },
            LayoutStyle.CREATIVE: {
                "heading": "Playfair Display",
                "body": "Lato",
                "code": "Monaco"
            },
            LayoutStyle.PROFESSIONAL: {
                "heading": "Merriweather",
                "body": "Open Sans",
                "code": "Source Code Pro"
            },
            LayoutStyle.MINIMAL: {
                "heading": "Inter",
                "body": "Inter",
                "code": "JetBrains Mono"
            },
            LayoutStyle.MODERN: {
                "heading": "Poppins",
                "body": "Inter",
                "code": "Fira Code"
            }
        }
        
        return typography_options.get(style, typography_options[LayoutStyle.MODERN])
    
    def get_available_schemes(self) -> List[str]:
        """Get list of available color schemes."""
        return list(self.color_schemes.keys())
    
    def preview_scheme(self, scheme_name: str) -> Optional[ColorScheme]:
        """Preview a specific color scheme."""
        return self.color_schemes.get(scheme_name)
