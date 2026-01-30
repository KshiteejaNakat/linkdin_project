"""
Profile Input Component
Handles user profile data collection.
"""

import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path


def render():
    """Render profile input form."""
    st.header("📝 Enter Your Profile Information")
    
    st.markdown("""
    Provide your professional information to get started. 
    You can upload documents or enter details manually.
    """)
    
    tab1, tab2, tab3 = st.tabs([
        "📄 Upload Documents",
        "🔗 LinkedIn URL",
        "✍️ Manual Entry"
    ])
    
    with tab1:
        render_upload_tab()
    
    with tab2:
        render_linkedin_tab()
    
    with tab3:
        render_manual_tab()


def render_upload_tab():
    """Render document upload interface."""
    st.subheader("Upload Your Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        resume_file = st.file_uploader(
            "Upload Resume (PDF, DOCX)",
            type=["pdf", "docx"],
            help="Your most recent resume"
        )
        
        if resume_file:
            st.success(f"✅ Uploaded: {resume_file.name}")
    
    with col2:
        portfolio_file = st.file_uploader(
            "Upload Portfolio (Optional)",
            type=["pdf", "zip"],
            help="Any existing portfolio materials"
        )
        
        if portfolio_file:
            st.success(f"✅ Uploaded: {portfolio_file.name}")
    
    github_url = st.text_input(
        "GitHub Profile URL (Optional)",
        placeholder="https://github.com/username"
    )
    
    if st.button("🚀 Analyze Documents", type="primary"):
        if resume_file:
            with st.spinner("Analyzing your profile..."):
                process_uploaded_documents(
                    resume_file,
                    portfolio_file,
                    github_url
                )
        else:
            st.warning("Please upload at least your resume.")


def render_linkedin_tab():
    """Render LinkedIn URL input."""
    st.subheader("Import from LinkedIn")
    
    st.info("""
    💡 **Tip**: For best results, export your LinkedIn profile data 
    and upload it in the Documents tab.
    """)
    
    linkedin_url = st.text_input(
        "LinkedIn Profile URL",
        placeholder="https://linkedin.com/in/username"
    )
    
    st.markdown("---")
    
    st.subheader("Or Upload LinkedIn Export")
    
    linkedin_export = st.file_uploader(
        "LinkedIn Data Export (ZIP)",
        type=["zip"],
        help="Download from LinkedIn Settings > Data Privacy"
    )
    
    if st.button("📥 Import LinkedIn Data", type="primary"):
        if linkedin_url or linkedin_export:
            with st.spinner("Importing LinkedIn data..."):
                process_linkedin_data(linkedin_url, linkedin_export)
        else:
            st.warning("Please provide LinkedIn URL or export file.")


def render_manual_tab():
    """Render manual entry form."""
    st.subheader("Manual Profile Entry")
    
    with st.form("manual_profile_form"):
        # Basic Info
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*")
            current_title = st.text_input("Current Job Title*")
        
        with col2:
            email = st.text_input("Email")
            location = st.text_input("Location")
        
        # Professional Summary
        st.markdown("### Professional Summary")
        summary = st.text_area(
            "About You",
            height=100,
            placeholder="Brief description of your professional background..."
        )
        
        # Experience
        st.markdown("### Experience (Most Recent)")
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            company = st.text_input("Company Name")
            role = st.text_input("Role/Title")
        
        with exp_col2:
            duration = st.text_input("Duration (e.g., 2020-Present)")
        
        responsibilities = st.text_area(
            "Key Responsibilities & Achievements",
            height=100,
            placeholder="List your main responsibilities..."
        )
        
        # Skills
        st.markdown("### Skills")
        skills = st.text_input(
            "Skills (comma-separated)",
            placeholder="Python, Project Management, Data Analysis..."
        )
        
        # Submit
        submitted = st.form_submit_button(
            "🚀 Start Analysis",
            type="primary"
        )
        
        if submitted:
            if name and current_title:
                process_manual_entry({
                    "name": name,
                    "title": current_title,
                    "email": email,
                    "location": location,
                    "summary": summary,
                    "experience": {
                        "company": company,
                        "role": role,
                        "duration": duration,
                        "responsibilities": responsibilities
                    },
                    "skills": [s.strip() for s in skills.split(",")]
                })
            else:
                st.warning("Please fill in required fields (*).")


def process_uploaded_documents(
    resume_file,
    portfolio_file,
    github_url: str
):
    """Process uploaded documents."""
    st.session_state.profile_data = {
        "source": "upload",
        "resume": resume_file.name if resume_file else None,
        "portfolio": portfolio_file.name if portfolio_file else None,
        "github": github_url
    }
    st.session_state.current_step = 1
    st.success("Profile data processed successfully!")
    st.rerun()


def process_linkedin_data(url: str, export_file):
    """Process LinkedIn data."""
    st.session_state.profile_data = {
        "source": "linkedin",
        "url": url,
        "export": export_file.name if export_file else None
    }
    st.session_state.current_step = 1
    st.success("LinkedIn data imported successfully!")
    st.rerun()


def process_manual_entry(data: Dict[str, Any]):
    """Process manually entered data."""
    st.session_state.profile_data = {
        "source": "manual",
        **data
    }
    st.session_state.current_step = 1
    st.success("Profile created successfully!")
    st.rerun()
