"""
Resume Parser Module
Extracts structured data from resume files.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import re
from loguru import logger


@dataclass
class ParsedResume:
    """Structured resume data."""
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    summary: str = ""
    experience: List[Dict] = field(default_factory=list)
    education: List[Dict] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    projects: List[Dict] = field(default_factory=list)


class ResumeParser:
    """
    Parses resumes from various formats (PDF, DOCX, TXT)
    and extracts structured career data.
    """
    
    def __init__(self):
        self.supported_formats = [".pdf", ".docx", ".doc", ".txt"]
        
    async def parse_resume(
        self, file_path: Optional[str] = None, 
        text_content: Optional[str] = None
    ) -> ParsedResume:
        """
        Parse resume from file or text content.
        """
        if file_path:
            text_content = await self._extract_text(file_path)
        
        if not text_content:
            logger.warning("No content to parse")
            return ParsedResume()
        
        return self._parse_content(text_content)
    
    async def _extract_text(self, file_path: str) -> str:
        """Extract text from file based on format."""
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return ""
        
        suffix = path.suffix.lower()
        
        if suffix == ".txt":
            return path.read_text(encoding="utf-8")
        elif suffix == ".pdf":
            return await self._extract_from_pdf(path)
        elif suffix in [".docx", ".doc"]:
            return await self._extract_from_docx(path)
        
        return ""
    
    async def _extract_from_pdf(self, path: Path) -> str:
        """Extract text from PDF file."""
        try:
            import pdfplumber
            
            text_parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            
            return "\n".join(text_parts)
        except ImportError:
            logger.warning("pdfplumber not installed")
            return ""
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""
    
    async def _extract_from_docx(self, path: Path) -> str:
        """Extract text from DOCX file."""
        try:
            from docx import Document
            
            doc = Document(path)
            return "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            logger.warning("python-docx not installed")
            return ""
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return ""
    
    def _parse_content(self, text: str) -> ParsedResume:
        """Parse text content into structured resume."""
        resume = ParsedResume()
        
        # Extract contact info
        resume.email = self._extract_email(text)
        resume.phone = self._extract_phone(text)
        resume.linkedin_url = self._extract_linkedin(text)
        resume.github_url = self._extract_github(text)
        resume.name = self._extract_name(text)
        
        # Extract sections
        sections = self._split_into_sections(text)
        
        resume.summary = sections.get("summary", "")
        resume.experience = self._parse_experience(sections.get("experience", ""))
        resume.education = self._parse_education(sections.get("education", ""))
        resume.skills = self._parse_skills(sections.get("skills", ""))
        resume.certifications = self._parse_certifications(sections.get("certifications", ""))
        resume.projects = self._parse_projects(sections.get("projects", ""))
        
        return resume
    
    def _extract_email(self, text: str) -> str:
        """Extract email address."""
        pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number."""
        pattern = r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL."""
        pattern = r'linkedin\.com/in/[\w-]+'
        match = re.search(pattern, text, re.IGNORECASE)
        return f"https://{match.group(0)}" if match else ""
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL."""
        pattern = r'github\.com/[\w-]+'
        match = re.search(pattern, text, re.IGNORECASE)
        return f"https://{match.group(0)}" if match else ""
    
    def _extract_name(self, text: str) -> str:
        """Extract name (usually first line)."""
        lines = text.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # Simple heuristic: name is likely short and at the top
            if len(first_line) < 50 and not '@' in first_line:
                return first_line
        return ""
    
    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split resume into sections."""
        sections = {}
        section_headers = {
            "summary": ["summary", "about", "profile", "objective"],
            "experience": ["experience", "work history", "employment"],
            "education": ["education", "academic"],
            "skills": ["skills", "technical skills", "competencies"],
            "certifications": ["certifications", "certificates", "licenses"],
            "projects": ["projects", "portfolio"]
        }
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            found_section = None
            for section, keywords in section_headers.items():
                if any(kw in line_lower for kw in keywords):
                    found_section = section
                    break
            
            if found_section:
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = found_section
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _parse_experience(self, text: str) -> List[Dict]:
        """Parse experience section."""
        experiences = []
        
        if not text:
            return experiences
        
        # Split by common patterns
        entries = re.split(r'\n(?=[A-Z][a-z]+\s+[A-Z])', text)
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
            
            lines = entry.strip().split('\n')
            if lines:
                exp = {
                    "title": lines[0].strip() if lines else "",
                    "company": lines[1].strip() if len(lines) > 1 else "",
                    "period": self._extract_date_range(entry),
                    "description": '\n'.join(lines[2:]) if len(lines) > 2 else ""
                }
                experiences.append(exp)
        
        return experiences[:10]  # Limit to 10 experiences
    
    def _parse_education(self, text: str) -> List[Dict]:
        """Parse education section."""
        education = []
        
        if not text:
            return education
        
        lines = text.strip().split('\n')
        current_edu = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_edu:
                    education.append(current_edu)
                    current_edu = {}
                continue
            
            if any(kw in line.lower() for kw in ["bachelor", "master", "phd", "degree"]):
                current_edu["degree"] = line
            elif any(kw in line.lower() for kw in ["university", "college", "institute"]):
                current_edu["institution"] = line
            else:
                date_range = self._extract_date_range(line)
                if date_range:
                    current_edu["period"] = date_range
        
        if current_edu:
            education.append(current_edu)
        
        return education
    
    def _parse_skills(self, text: str) -> List[str]:
        """Parse skills section."""
        if not text:
            return []
        
        # Common skill separators
        skills = re.split(r'[,\n•\|;]', text)
        
        cleaned_skills = []
        for skill in skills:
            cleaned = skill.strip()
            if cleaned and len(cleaned) > 1 and len(cleaned) < 50:
                cleaned_skills.append(cleaned)
        
        return cleaned_skills[:30]  # Limit to 30 skills
    
    def _parse_certifications(self, text: str) -> List[str]:
        """Parse certifications section."""
        if not text:
            return []
        
        certs = text.strip().split('\n')
        return [c.strip() for c in certs if c.strip()][:10]
    
    def _parse_projects(self, text: str) -> List[Dict]:
        """Parse projects section."""
        projects = []
        
        if not text:
            return projects
        
        entries = text.strip().split('\n\n')
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
            
            lines = entry.strip().split('\n')
            project = {
                "name": lines[0].strip() if lines else "",
                "description": '\n'.join(lines[1:]) if len(lines) > 1 else ""
            }
            projects.append(project)
        
        return projects[:10]
    
    def _extract_date_range(self, text: str) -> str:
        """Extract date range from text."""
        patterns = [
            r'\d{4}\s*[-–]\s*\d{4}',
            r'\d{4}\s*[-–]\s*[Pp]resent',
            r'[A-Za-z]+\s+\d{4}\s*[-–]\s*[A-Za-z]+\s+\d{4}',
            r'[A-Za-z]+\s+\d{4}\s*[-–]\s*[Pp]resent'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return ""
