"""
Results Display Component
Displays Career DNA and analysis results.
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_career_dna():
    """Render Career DNA analysis results."""
    st.header("🧬 Your Career DNA")
    
    if not st.session_state.profile_data:
        st.warning("Please complete the profile input step first.")
        if st.button("← Go Back"):
            st.session_state.current_step = 0
            st.rerun()
        return
    
    # Simulate Career DNA analysis
    with st.spinner("Analyzing your Career DNA..."):
        career_dna = analyze_career_dna(st.session_state.profile_data)
        st.session_state.career_dna = career_dna
    
    # Display results
    render_dna_overview(career_dna)
    render_skills_analysis(career_dna.get("skills", {}))
    render_career_trajectory(career_dna.get("trajectory", {}))
    render_market_fit(career_dna.get("market_fit", {}))
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to Profile"):
            st.session_state.current_step = 0
            st.rerun()
    
    with col2:
        if st.button("Continue to Optimization →", type="primary"):
            st.session_state.current_step = 2
            st.rerun()


def analyze_career_dna(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze profile and generate Career DNA."""
    # Simulated analysis - in production, calls actual agents
    return {
        "core_identity": {
            "archetype": "Technical Leader",
            "strengths": ["Problem Solving", "Innovation", "Team Leadership"],
            "differentiators": ["Cross-functional expertise", "Data-driven"]
        },
        "skills": {
            "technical": [
                {"name": "Python", "level": 90},
                {"name": "Machine Learning", "level": 85},
                {"name": "Cloud Architecture", "level": 80}
            ],
            "soft": [
                {"name": "Leadership", "level": 85},
                {"name": "Communication", "level": 80},
                {"name": "Strategic Thinking", "level": 75}
            ]
        },
        "trajectory": {
            "current_level": "Senior",
            "years_experience": 7,
            "growth_rate": "Above Average",
            "next_roles": ["Principal Engineer", "Engineering Manager"]
        },
        "market_fit": {
            "demand_score": 85,
            "salary_percentile": 75,
            "trending_skills": ["GenAI", "LLMs", "MLOps"]
        }
    }


def render_dna_overview(career_dna: Dict[str, Any]):
    """Render Career DNA overview section."""
    st.subheader("🎯 Core Identity")
    
    identity = career_dna.get("core_identity", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Archetype",
            identity.get("archetype", "Professional")
        )
    
    with col2:
        strengths = identity.get("strengths", [])
        st.markdown("**Top Strengths**")
        for s in strengths[:3]:
            st.markdown(f"• {s}")
    
    with col3:
        differentiators = identity.get("differentiators", [])
        st.markdown("**Differentiators**")
        for d in differentiators[:3]:
            st.markdown(f"• {d}")


def render_skills_analysis(skills: Dict[str, Any]):
    """Render skills breakdown."""
    st.subheader("💡 Skills Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Technical Skills**")
        technical = skills.get("technical", [])
        for skill in technical:
            st.progress(skill["level"] / 100)
            st.caption(f"{skill['name']}: {skill['level']}%")
    
    with col2:
        st.markdown("**Soft Skills**")
        soft = skills.get("soft", [])
        for skill in soft:
            st.progress(skill["level"] / 100)
            st.caption(f"{skill['name']}: {skill['level']}%")


def render_career_trajectory(trajectory: Dict[str, Any]):
    """Render career trajectory analysis."""
    st.subheader("📈 Career Trajectory")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Level", trajectory.get("current_level", "N/A"))
    
    with col2:
        st.metric("Experience", f"{trajectory.get('years_experience', 0)} years")
    
    with col3:
        st.metric("Growth Rate", trajectory.get("growth_rate", "N/A"))
    
    with col4:
        next_roles = trajectory.get("next_roles", [])
        st.markdown("**Next Steps**")
        for role in next_roles[:2]:
            st.markdown(f"→ {role}")


def render_market_fit(market_fit: Dict[str, Any]):
    """Render market fit analysis."""
    st.subheader("📊 Market Fit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        demand_score = market_fit.get("demand_score", 0)
        st.metric(
            "Market Demand",
            f"{demand_score}%",
            delta="High" if demand_score > 70 else "Moderate"
        )
        
        salary = market_fit.get("salary_percentile", 0)
        st.metric(
            "Salary Percentile",
            f"Top {100 - salary}%"
        )
    
    with col2:
        st.markdown("**Trending Skills to Add**")
        trending = market_fit.get("trending_skills", [])
        for skill in trending:
            st.markdown(f"🔥 {skill}")
        
        st.info("Adding these skills could increase your market value by 15-25%")
