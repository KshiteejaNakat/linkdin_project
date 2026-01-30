"""
React Portfolio Generator Module
Generates React-based portfolio code from content and layout.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
from loguru import logger
import json


@dataclass
class GeneratedPortfolio:
    """Generated portfolio files."""
    files: Dict[str, str]  # filename -> content
    entry_point: str
    build_instructions: str
    preview_html: str


class ReactPortfolioGenerator:
    """
    Generates React portfolio code from content and layout configuration.
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir
        
    def generate(
        self,
        content: Dict,
        layout_config: Dict,
        output_format: str = "react"
    ) -> GeneratedPortfolio:
        """Generate complete portfolio code."""
        
        files = {}
        
        # Generate main App component
        files["App.jsx"] = self._generate_app_component(content, layout_config)
        
        # Generate section components
        files["components/Hero.jsx"] = self._generate_hero_component(content, layout_config)
        files["components/About.jsx"] = self._generate_about_component(content)
        files["components/Skills.jsx"] = self._generate_skills_component(content)
        files["components/Projects.jsx"] = self._generate_projects_component(content)
        files["components/Experience.jsx"] = self._generate_experience_component(content)
        files["components/Contact.jsx"] = self._generate_contact_component(content)
        
        # Generate styles
        files["styles/globals.css"] = self._generate_global_styles(layout_config)
        
        # Generate package.json
        files["package.json"] = self._generate_package_json(content)
        
        # Generate index.html
        files["index.html"] = self._generate_index_html(content)
        
        # Build instructions
        instructions = self._generate_build_instructions()
        
        # Preview HTML (single file)
        preview = self._generate_preview_html(content, layout_config)
        
        return GeneratedPortfolio(
            files=files,
            entry_point="App.jsx",
            build_instructions=instructions,
            preview_html=preview
        )
    
    def _generate_app_component(self, content: Dict, layout: Dict) -> str:
        """Generate main App component."""
        sections = layout.get("sections", ["hero", "about", "skills", "projects", "contact"])
        
        imports = [
            "import React from 'react';",
            "import './styles/globals.css';"
        ]
        
        components = []
        for section in sections:
            component_name = section.capitalize()
            imports.append(f"import {component_name} from './components/{component_name}';")
            components.append(f"      <{component_name} />")
        
        return f"""{chr(10).join(imports)}

function App() {{
  return (
    <div className="portfolio">
{chr(10).join(components)}
    </div>
  );
}}

export default App;
"""
    
    def _generate_hero_component(self, content: Dict, layout: Dict) -> str:
        """Generate Hero section component."""
        hero = content.get("hero", {})
        colors = layout.get("colors", {})
        
        return f"""import React from 'react';

const Hero = () => {{
  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <h1 className="hero-name">{hero.get('name', 'Your Name')}</h1>
        <h2 className="hero-title">{hero.get('title', 'Professional')}</h2>
        <p className="hero-tagline">{hero.get('tagline', '')}</p>
        <p className="hero-description">{hero.get('description', '')}</p>
        <div className="hero-cta">
          <a href="#projects" className="btn btn-primary">
            {hero.get('cta_primary', 'View My Work')}
          </a>
          <a href="#contact" className="btn btn-secondary">
            {hero.get('cta_secondary', 'Contact Me')}
          </a>
        </div>
      </div>
    </section>
  );
}};

export default Hero;
"""
    
    def _generate_about_component(self, content: Dict) -> str:
        """Generate About section component."""
        about = content.get("about", "")
        
        return f"""import React from 'react';

const About = () => {{
  return (
    <section className="about" id="about">
      <div className="container">
        <h2 className="section-title">About Me</h2>
        <div className="about-content">
          <p>{about}</p>
        </div>
      </div>
    </section>
  );
}};

export default About;
"""
    
    def _generate_skills_component(self, content: Dict) -> str:
        """Generate Skills section component."""
        skills = content.get("skills", {})
        
        skills_json = json.dumps(skills, indent=2)
        
        return f"""import React from 'react';

const skillsData = {skills_json};

const Skills = () => {{
  return (
    <section className="skills" id="skills">
      <div className="container">
        <h2 className="section-title">Skills</h2>
        <div className="skills-grid">
          {{Object.entries(skillsData).map(([category, items]) => (
            <div key={{category}} className="skill-category">
              <h3>{{category}}</h3>
              <div className="skill-tags">
                {{items.map((skill, idx) => (
                  <span key={{idx}} className="skill-tag">{{skill}}</span>
                ))}}
              </div>
            </div>
          ))}}
        </div>
      </div>
    </section>
  );
}};

export default Skills;
"""
    
    def _generate_projects_component(self, content: Dict) -> str:
        """Generate Projects section component."""
        projects = content.get("projects", [])
        
        projects_data = []
        for p in projects:
            projects_data.append({
                "title": p.get("title", ""),
                "description": p.get("description", ""),
                "technologies": p.get("technologies", []),
                "github_url": p.get("github_url", ""),
                "live_url": p.get("live_url", "")
            })
        
        projects_json = json.dumps(projects_data, indent=2)
        
        return f"""import React from 'react';

const projectsData = {projects_json};

const Projects = () => {{
  return (
    <section className="projects" id="projects">
      <div className="container">
        <h2 className="section-title">Projects</h2>
        <div className="projects-grid">
          {{projectsData.map((project, idx) => (
            <div key={{idx}} className="project-card">
              <h3>{{project.title}}</h3>
              <p>{{project.description}}</p>
              <div className="project-tech">
                {{project.technologies.map((tech, i) => (
                  <span key={{i}} className="tech-tag">{{tech}}</span>
                ))}}
              </div>
              <div className="project-links">
                {{project.github_url && (
                  <a href={{project.github_url}} target="_blank" rel="noreferrer">
                    GitHub
                  </a>
                )}}
                {{project.live_url && (
                  <a href={{project.live_url}} target="_blank" rel="noreferrer">
                    Live Demo
                  </a>
                )}}
              </div>
            </div>
          ))}}
        </div>
      </div>
    </section>
  );
}};

export default Projects;
"""
    
    def _generate_experience_component(self, content: Dict) -> str:
        """Generate Experience section component."""
        experience = content.get("experience", [])
        
        exp_data = []
        for e in experience:
            exp_data.append({
                "title": e.get("title", ""),
                "company": e.get("company", ""),
                "period": e.get("period", ""),
                "highlights": e.get("highlights", [])
            })
        
        exp_json = json.dumps(exp_data, indent=2)
        
        return f"""import React from 'react';

const experienceData = {exp_json};

const Experience = () => {{
  return (
    <section className="experience" id="experience">
      <div className="container">
        <h2 className="section-title">Experience</h2>
        <div className="timeline">
          {{experienceData.map((exp, idx) => (
            <div key={{idx}} className="timeline-item">
              <div className="timeline-content">
                <h3>{{exp.title}}</h3>
                <h4>{{exp.company}}</h4>
                <span className="period">{{exp.period}}</span>
                <ul>
                  {{exp.highlights.map((h, i) => (
                    <li key={{i}}>{{h}}</li>
                  ))}}
                </ul>
              </div>
            </div>
          ))}}
        </div>
      </div>
    </section>
  );
}};

export default Experience;
"""
    
    def _generate_contact_component(self, content: Dict) -> str:
        """Generate Contact section component."""
        contact = content.get("contact", {})
        
        return f"""import React from 'react';

const Contact = () => {{
  return (
    <section className="contact" id="contact">
      <div className="container">
        <h2 className="section-title">Get In Touch</h2>
        <div className="contact-content">
          <p>I'm always open to new opportunities and collaborations.</p>
          <div className="contact-links">
            <a href="mailto:{contact.get('email', '')}" className="contact-link">
              Email Me
            </a>
            <a href="{contact.get('linkedin', '')}" target="_blank" rel="noreferrer">
              LinkedIn
            </a>
            <a href="{contact.get('github', '')}" target="_blank" rel="noreferrer">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}};

export default Contact;
"""
    
    def _generate_global_styles(self, layout: Dict) -> str:
        """Generate global CSS styles."""
        colors = layout.get("colors", {})
        
        return f"""/* Portfolio Global Styles */
:root {{
  --primary: {colors.get('primary', '#2563eb')};
  --secondary: {colors.get('secondary', '#64748b')};
  --accent: {colors.get('accent', '#0ea5e9')};
  --background: {colors.get('background', '#ffffff')};
  --surface: {colors.get('surface', '#f8fafc')};
  --text-primary: {colors.get('text_primary', '#0f172a')};
  --text-secondary: {colors.get('text_secondary', '#475569')};
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: 'Inter', sans-serif;
  background: var(--background);
  color: var(--text-primary);
  line-height: 1.6;
}}

.container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}}

section {{
  padding: 5rem 0;
}}

.section-title {{
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
}}

/* Hero Section */
.hero {{
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: var(--surface);
}}

.hero-name {{
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
}}

.hero-title {{
  font-size: 1.5rem;
  color: var(--primary);
  margin-bottom: 1rem;
}}

.hero-tagline {{
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}}

.hero-cta {{
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}}

/* Buttons */
.btn {{
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}}

.btn-primary {{
  background: var(--primary);
  color: white;
}}

.btn-secondary {{
  border: 2px solid var(--primary);
  color: var(--primary);
}}

/* Skills */
.skills-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}}

.skill-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}}

.skill-tag {{
  background: var(--surface);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
}}

/* Projects */
.projects-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}}

.project-card {{
  background: var(--surface);
  padding: 2rem;
  border-radius: 1rem;
  transition: transform 0.3s ease;
}}

.project-card:hover {{
  transform: translateY(-5px);
}}

/* Timeline */
.timeline {{
  position: relative;
  padding-left: 2rem;
}}

.timeline::before {{
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--primary);
}}

.timeline-item {{
  position: relative;
  margin-bottom: 2rem;
  padding-left: 1.5rem;
}}

/* Contact */
.contact {{
  text-align: center;
  background: var(--surface);
}}

.contact-links {{
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}}

.contact-link {{
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}}
"""
    
    def _generate_package_json(self, content: Dict) -> str:
        """Generate package.json."""
        name = content.get("hero", {}).get("name", "portfolio").lower().replace(" ", "-")
        
        return json.dumps({
            "name": f"{name}-portfolio",
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build"
            }
        }, indent=2)
    
    def _generate_index_html(self, content: Dict) -> str:
        """Generate index.html."""
        name = content.get("hero", {}).get("name", "Portfolio")
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <div id="root"></div>
</body>
</html>
"""
    
    def _generate_build_instructions(self) -> str:
        """Generate build instructions."""
        return """# Portfolio Build Instructions

1. Install dependencies:
   npm install

2. Start development server:
   npm start

3. Build for production:
   npm run build

4. Deploy the 'build' folder to your hosting provider.
"""
    
    def _generate_preview_html(self, content: Dict, layout: Dict) -> str:
        """Generate single-file preview HTML."""
        hero = content.get("hero", {})
        colors = layout.get("colors", {})
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{hero.get('name', 'Portfolio')} | Preview</title>
  <style>
    :root {{
      --primary: {colors.get('primary', '#2563eb')};
      --bg: {colors.get('background', '#ffffff')};
      --text: {colors.get('text_primary', '#0f172a')};
    }}
    body {{ font-family: Inter, sans-serif; background: var(--bg); color: var(--text); margin: 0; }}
    .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; }}
    h1 {{ font-size: 3rem; margin-bottom: 0.5rem; }}
    h2 {{ color: var(--primary); font-size: 1.5rem; }}
    p {{ color: #64748b; max-width: 600px; margin: 1rem auto; }}
  </style>
</head>
<body>
  <section class="hero">
    <div>
      <h1>{hero.get('name', 'Your Name')}</h1>
      <h2>{hero.get('title', 'Professional')}</h2>
      <p>{hero.get('tagline', '')}</p>
    </div>
  </section>
</body>
</html>
"""
