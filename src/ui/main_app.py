"""
Main Streamlit Application
Entry point for the Adaptive AI Career Architect.
"""

import streamlit as st
from pathlib import Path
import asyncio
from typing import Dict, Any, Optional

# Page configuration must be first Streamlit command
st.set_page_config(
    page_title="Adaptive AI Career Architect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    defaults = {
        "current_step": 0,
        "profile_data": None,
        "career_dna": None,
        "optimization_results": None,
        "portfolio_data": None,
        "processing": False,
        "error_message": None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header():
    """Render application header."""
    st.title("🚀 Adaptive AI Career Architect")
    st.markdown("""
    *Transform your professional presence with AI-powered optimization*
    
    ---
    """)


def render_sidebar():
    """Render sidebar with navigation and settings."""
    with st.sidebar:
        st.header("📍 Navigation")
        
        steps = [
            "1️⃣ Input Profile",
            "2️⃣ Career DNA Analysis",
            "3️⃣ LinkedIn Optimization",
            "4️⃣ Portfolio Generation",
            "5️⃣ Review & Export"
        ]
        
        for i, step in enumerate(steps):
            if i == st.session_state.current_step:
                st.markdown(f"**→ {step}**")
            elif i < st.session_state.current_step:
                st.markdown(f"✅ {step}")
            else:
                st.markdown(f"○ {step}")
        
        st.markdown("---")
        
        st.header("⚙️ Settings")
        
        industry = st.selectbox(
            "Target Industry",
            ["Technology", "Finance", "Healthcare", "Marketing", 
             "Consulting", "Education", "Other"]
        )
        
        optimization_level = st.slider(
            "Optimization Intensity",
            min_value=1,
            max_value=10,
            value=7,
            help="Higher values = more aggressive optimization"
        )
        
        include_portfolio = st.checkbox(
            "Generate Portfolio Website",
            value=True
        )
        
        st.markdown("---")
        
        st.header("📊 Progress")
        progress = (st.session_state.current_step / 4) * 100
        st.progress(int(progress))
        st.caption(f"{int(progress)}% Complete")
        
        return {
            "industry": industry,
            "optimization_level": optimization_level,
            "include_portfolio": include_portfolio
        }


def render_step_indicator():
    """Render current step indicator."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    steps = [
        (col1, "Input", 0),
        (col2, "DNA", 1),
        (col3, "Optimize", 2),
        (col4, "Portfolio", 3),
        (col5, "Export", 4)
    ]
    
    for col, name, idx in steps:
        with col:
            if idx < st.session_state.current_step:
                st.success(f"✅ {name}")
            elif idx == st.session_state.current_step:
                st.info(f"🔵 {name}")
            else:
                st.empty()
                st.caption(f"○ {name}")


def render_main_content(settings: Dict[str, Any]):
    """Render main content area based on current step."""
    from .components import (
        profile_input,
        results_display,
        portfolio_preview,
        optimization_panel
    )
    
    render_step_indicator()
    st.markdown("---")
    
    step = st.session_state.current_step
    
    if step == 0:
        profile_input.render()
    elif step == 1:
        results_display.render_career_dna()
    elif step == 2:
        optimization_panel.render()
    elif step == 3:
        portfolio_preview.render()
    elif step == 4:
        render_export_step()


def render_export_step():
    """Render final export step."""
    st.header("📤 Export Your Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("LinkedIn Content")
        if st.session_state.optimization_results:
            st.download_button(
                "📥 Download LinkedIn Content",
                data="LinkedIn content here",
                file_name="linkedin_content.txt",
                mime="text/plain"
            )
    
    with col2:
        st.subheader("Portfolio Website")
        if st.session_state.portfolio_data:
            st.download_button(
                "📥 Download Portfolio (ZIP)",
                data=b"Portfolio ZIP content",
                file_name="portfolio.zip",
                mime="application/zip"
            )
    
    st.markdown("---")
    
    if st.button("🔄 Start New Analysis", type="primary"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()


def render_error():
    """Render error message if present."""
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        if st.button("Dismiss"):
            st.session_state.error_message = None
            st.rerun()


def run_app():
    """Main application entry point."""
    init_session_state()
    render_header()
    render_error()
    settings = render_sidebar()
    render_main_content(settings)


if __name__ == "__main__":
    run_app()
