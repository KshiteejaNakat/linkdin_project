"""
Portfolio Preview Component
Displays generated portfolio website preview.
"""

import streamlit as st
from typing import Dict, Any, Optional
import json


def render():
    """Render portfolio generation and preview."""
    st.header("🎨 Portfolio Generation")
    
    if not st.session_state.optimization_results:
        st.warning("Please complete LinkedIn optimization first.")
        if st.button("← Go Back"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    # Portfolio configuration
    render_portfolio_config()
    
    # Generate or show preview
    if st.session_state.portfolio_data:
        render_portfolio_preview()
    else:
        if st.button("🎨 Generate Portfolio", type="primary"):
            with st.spinner("Generating your portfolio..."):
                portfolio = generate_portfolio(
                    st.session_state.career_dna,
                    st.session_state.optimization_results
                )
                st.session_state.portfolio_data = portfolio
                st.rerun()
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to Optimization"):
            st.session_state.current_step = 2
            st.rerun()
    
    with col2:
        if st.session_state.portfolio_data:
            if st.button("Export Results →", type="primary"):
                st.session_state.current_step = 4
                st.rerun()


def render_portfolio_config():
    """Render portfolio configuration options."""
    with st.expander("⚙️ Portfolio Settings", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            layout = st.selectbox(
                "Layout Style",
                ["Modern Minimal", "Creative Bold", "Professional Classic"]
            )
        
        with col2:
            color_scheme = st.selectbox(
                "Color Scheme",
                ["Blue Professional", "Dark Mode", "Light Elegant", "Custom"]
            )
        
        with col3:
            sections = st.multiselect(
                "Include Sections",
                ["Hero", "About", "Skills", "Experience", "Projects", "Contact"],
                default=["Hero", "About", "Skills", "Experience", "Contact"]
            )


def generate_portfolio(
    career_dna: Dict[str, Any],
    optimizations: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate portfolio content."""
    identity = career_dna.get("core_identity", {})
    
    return {
        "layout": "modern_minimal",
        "color_scheme": "blue_professional",
        "content": {
            "hero": {
                "title": identity.get("archetype", "Professional"),
                "subtitle": "Building the future, one line of code at a time",
                "cta": "View My Work"
            },
            "about": optimizations.get("about", {}).get("optimized", ""),
            "skills": career_dna.get("skills", {}),
            "experience": optimizations.get("experience", []),
            "projects": [
                {
                    "name": "AI Career Architect",
                    "description": "AI-powered career optimization platform",
                    "tech": ["Python", "Streamlit", "HuggingFace"],
                    "link": "#"
                }
            ],
            "contact": {
                "email": "contact@example.com",
                "linkedin": "linkedin.com/in/username",
                "github": "github.com/username"
            }
        },
        "files": {
            "App.jsx": "// React App Component",
            "Hero.jsx": "// Hero Section",
            "About.jsx": "// About Section",
            "Skills.jsx": "// Skills Section",
            "Experience.jsx": "// Experience Section",
            "Contact.jsx": "// Contact Section",
            "styles.css": "/* Portfolio Styles */"
        }
    }


def render_portfolio_preview():
    """Render portfolio preview."""
    portfolio = st.session_state.portfolio_data
    content = portfolio.get("content", {})
    
    st.subheader("📱 Portfolio Preview")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Preview", "Code Files", "Download"])
    
    with tab1:
        render_visual_preview(content)
    
    with tab2:
        render_code_files(portfolio.get("files", {}))
    
    with tab3:
        render_download_options(portfolio)


def render_visual_preview(content: Dict[str, Any]):
    """Render visual portfolio preview."""
    # Simulated browser frame
    st.markdown("""
    <style>
    .portfolio-preview {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    hero = content.get("hero", {})
    
    st.markdown(f"""
    ### 🎯 {hero.get('title', 'Your Name')}
    *{hero.get('subtitle', 'Your tagline')}*
    """)
    
    st.button(hero.get('cta', 'Contact Me'))
    
    st.markdown("---")
    
    # About preview
    st.markdown("**About**")
    about_text = content.get("about", "")
    st.markdown(about_text[:500] + "..." if len(about_text) > 500 else about_text)
    
    st.markdown("---")
    
    # Skills preview
    st.markdown("**Skills**")
    skills = content.get("skills", {})
    technical = skills.get("technical", [])
    
    cols = st.columns(len(technical[:4]))
    for col, skill in zip(cols, technical[:4]):
        with col:
            st.metric(skill.get("name", ""), f"{skill.get('level', 0)}%")


def render_code_files(files: Dict[str, str]):
    """Render generated code files."""
    st.markdown("**Generated React Components**")
    
    selected_file = st.selectbox(
        "Select File",
        list(files.keys())
    )
    
    if selected_file:
        st.code(files.get(selected_file, ""), language="jsx")


def render_download_options(portfolio: Dict[str, Any]):
    """Render download options."""
    st.markdown("**Download Your Portfolio**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            "📦 Download React Project (ZIP)",
            data=json.dumps(portfolio, indent=2).encode(),
            file_name="portfolio-react.zip",
            mime="application/zip"
        )
    
    with col2:
        st.download_button(
            "📄 Download as HTML",
            data="<html><body>Portfolio HTML</body></html>",
            file_name="portfolio.html",
            mime="text/html"
        )
    
    st.markdown("---")
    
    st.info("""
    💡 **Deployment Options:**
    - Deploy to Vercel, Netlify, or GitHub Pages
    - Use the React project for full customization
    - Use the HTML version for quick static hosting
    """)
