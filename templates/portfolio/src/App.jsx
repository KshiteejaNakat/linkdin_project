import React from 'react';
import Hero from './components/Hero';
import About from './components/About';
import Skills from './components/Skills';
import Experience from './components/Experience';
import Projects from './components/Projects';
import Contact from './components/Contact';
import Navigation from './components/Navigation';

// Portfolio data - will be replaced by AI generation
const portfolioData = {
  name: "{{NAME}}",
  title: "{{TITLE}}",
  tagline: "{{TAGLINE}}",
  about: "{{ABOUT}}",
  skills: {{SKILLS_JSON}},
  experience: {{EXPERIENCE_JSON}},
  projects: {{PROJECTS_JSON}},
  contact: {
    email: "{{EMAIL}}",
    linkedin: "{{LINKEDIN}}",
    github: "{{GITHUB}}"
  }
};

function App() {
  return (
    <div className="min-h-screen bg-dark-300">
      <Navigation />
      <main>
        <Hero 
          name={portfolioData.name}
          title={portfolioData.title}
          tagline={portfolioData.tagline}
        />
        <About content={portfolioData.about} />
        <Skills skills={portfolioData.skills} />
        <Experience experiences={portfolioData.experience} />
        <Projects projects={portfolioData.projects} />
        <Contact contact={portfolioData.contact} />
      </main>
      <footer className="py-6 text-center text-gray-500">
        <p>Built with AI Career Architect</p>
      </footer>
    </div>
  );
}

export default App;
