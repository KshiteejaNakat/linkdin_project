"""
Optimization Panel Component
Displays LinkedIn optimization suggestions.
"""

import streamlit as st
from typing import Dict, Any, List


def render():
    """Render LinkedIn optimization panel."""
    st.header("✨ LinkedIn Optimization")
    
    if not st.session_state.career_dna:
        st.warning("Please complete the Career DNA analysis first.")
        if st.button("← Go Back"):
            st.session_state.current_step = 1
            st.rerun()
        return
    
    # Generate optimizations
    with st.spinner("Generating optimized content..."):
        optimizations = generate_optimizations(st.session_state.career_dna)
        st.session_state.optimization_results = optimizations
    
    # Display optimization sections
    render_headline_optimization(optimizations.get("headline", {}))
    render_about_optimization(optimizations.get("about", {}))
    render_experience_optimization(optimizations.get("experience", []))
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to DNA"):
            st.session_state.current_step = 1
            st.rerun()
    
    with col2:
        if st.button("Generate Portfolio →", type="primary"):
            st.session_state.current_step = 3
            st.rerun()


def generate_optimizations(career_dna: Dict[str, Any]) -> Dict[str, Any]:
    """Generate LinkedIn optimizations based on Career DNA."""
    identity = career_dna.get("core_identity", {})
    archetype = identity.get("archetype", "Professional")
    
    return {
        "headline": {
            "original": "Software Engineer at Company",
            "suggestions": [
                {
                    "text": f"{archetype} | Building Scalable AI Solutions | Python & ML Expert",
                    "score": 92,
                    "improvement": "+45% visibility"
                },
                {
                    "text": "Senior Engineer → Tech Lead | AI/ML | Helping teams ship faster",
                    "score": 88,
                    "improvement": "+38% visibility"
                },
                {
                    "text": "From Code to Impact | Data-Driven Engineering Leader",
                    "score": 85,
                    "improvement": "+32% visibility"
                }
            ]
        },
        "about": {
            "original": "I am a software engineer with experience...",
            "optimized": generate_about_text(career_dna),
            "improvements": [
                "Added compelling hook",
                "Included quantified achievements",
                "Added clear value proposition",
                "Optimized for keywords"
            ]
        },
        "experience": [
            {
                "role": "Senior Software Engineer",
                "company": "Tech Corp",
                "original": "Worked on backend systems",
                "optimized": "Led development of microservices architecture serving 10M+ users, reducing latency by 40% and costs by $200K annually",
                "keywords_added": ["microservices", "scalability", "cost optimization"]
            }
        ]
    }


def generate_about_text(career_dna: Dict[str, Any]) -> str:
    """Generate optimized About section."""
    identity = career_dna.get("core_identity", {})
    archetype = identity.get("archetype", "Professional")
    
    return f"""🚀 {archetype} passionate about building technology that matters.

I believe great engineering is about more than code—it's about solving real problems for real people. With 7+ years of experience, I've helped companies:

✅ Scale systems from startup to enterprise (10K → 10M users)
✅ Build AI/ML solutions that drive measurable business impact
✅ Lead high-performing teams through complex technical challenges

What sets me apart:
• Data-driven approach to decision making
• Bridge between technical depth and business strategy
• Track record of delivering 40%+ efficiency improvements

Currently exploring opportunities in AI/ML leadership roles.

Let's connect! Always happy to chat about technology, leadership, or your next big project.

📧 Open to: Full-time roles, Advisory, Speaking opportunities"""


def render_headline_optimization(headline_data: Dict[str, Any]):
    """Render headline optimization section."""
    st.subheader("📌 Headline Optimization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Current Headline**")
        st.error(headline_data.get("original", "No headline"))
    
    with col2:
        st.markdown("**Suggested Headlines**")
        suggestions = headline_data.get("suggestions", [])
        
        for i, suggestion in enumerate(suggestions):
            with st.container():
                cols = st.columns([3, 1, 1])
                
                with cols[0]:
                    st.success(suggestion["text"])
                
                with cols[1]:
                    st.metric("Score", f"{suggestion['score']}%")
                
                with cols[2]:
                    st.caption(suggestion["improvement"])
                
                if st.button(f"Use This", key=f"headline_{i}"):
                    st.session_state.optimization_results["headline"]["selected"] = i
                    st.success("Headline selected!")


def render_about_optimization(about_data: Dict[str, Any]):
    """Render About section optimization."""
    st.subheader("📝 About Section")
    
    tab1, tab2 = st.tabs(["Before & After", "Improvements"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original**")
            st.text_area(
                "Current About",
                about_data.get("original", ""),
                height=200,
                disabled=True,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Optimized**")
            optimized = st.text_area(
                "Optimized About",
                about_data.get("optimized", ""),
                height=200,
                label_visibility="collapsed"
            )
    
    with tab2:
        st.markdown("**Key Improvements**")
        improvements = about_data.get("improvements", [])
        
        for improvement in improvements:
            st.markdown(f"✅ {improvement}")


def render_experience_optimization(experiences: List[Dict[str, Any]]):
    """Render experience optimization suggestions."""
    st.subheader("💼 Experience Optimization")
    
    for exp in experiences:
        with st.expander(f"{exp['role']} at {exp['company']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original**")
                st.warning(exp.get("original", ""))
            
            with col2:
                st.markdown("**Optimized**")
                st.success(exp.get("optimized", ""))
            
            keywords = exp.get("keywords_added", [])
            if keywords:
                st.markdown("**Keywords Added:** " + ", ".join(
                    [f"`{k}`" for k in keywords]
                ))
