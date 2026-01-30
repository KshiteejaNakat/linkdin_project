"""
UI Module
Streamlit-based user interface components.
"""

from .main_app import run_app
from .components import (
    profile_input,
    results_display,
    portfolio_preview,
    optimization_panel
)

__all__ = [
    "run_app",
    "profile_input",
    "results_display",
    "portfolio_preview",
    "optimization_panel"
]
