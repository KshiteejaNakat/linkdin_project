"""
GitHub Analyzer Module
Analyzes GitHub profiles and repositories for career insights.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class GitHubProject:
    """Represents a GitHub project."""
    name: str
    description: str
    language: str
    stars: int
    forks: int
    topics: List[str]
    url: str
    is_featured: bool = False


@dataclass
class GitHubProfile:
    """Represents a GitHub profile analysis."""
    username: str
    name: str
    bio: str
    public_repos: int
    followers: int
    following: int
    top_languages: List[str]
    contribution_score: int
    projects: List[GitHubProject]


class GitHubAnalyzer:
    """
    Analyzes GitHub profiles to extract technical skills,
    project portfolio, and contribution patterns.
    """
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.api_base = "https://api.github.com"
        
    async def analyze_profile(self, username: str) -> Optional[GitHubProfile]:
        """Analyze a GitHub profile."""
        logger.info(f"Analyzing GitHub profile: {username}")
        
        try:
            if self.access_token:
                return await self._fetch_profile_api(username)
            else:
                return self._get_sample_profile(username)
        except Exception as e:
            logger.error(f"GitHub analysis error: {e}")
            return None
    
    async def _fetch_profile_api(self, username: str) -> GitHubProfile:
        """Fetch profile using GitHub API."""
        try:
            from github import Github
            
            g = Github(self.access_token)
            user = g.get_user(username)
            
            repos = list(user.get_repos())
            
            # Analyze repositories
            languages = {}
            projects = []
            
            for repo in repos[:20]:  # Limit to 20 repos
                # Count languages
                if repo.language:
                    languages[repo.language] = languages.get(repo.language, 0) + 1
                
                # Create project entry
                projects.append(GitHubProject(
                    name=repo.name,
                    description=repo.description or "",
                    language=repo.language or "",
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    topics=repo.get_topics(),
                    url=repo.html_url,
                    is_featured=repo.stargazers_count > 10
                ))
            
            # Sort languages by frequency
            top_languages = sorted(languages.keys(), key=lambda x: languages[x], reverse=True)[:5]
            
            return GitHubProfile(
                username=username,
                name=user.name or username,
                bio=user.bio or "",
                public_repos=user.public_repos,
                followers=user.followers,
                following=user.following,
                top_languages=top_languages,
                contribution_score=self._calculate_contribution_score(user, repos),
                projects=sorted(projects, key=lambda x: x.stars, reverse=True)
            )
            
        except ImportError:
            logger.warning("PyGithub not installed")
            return self._get_sample_profile(username)
    
    def _get_sample_profile(self, username: str) -> GitHubProfile:
        """Return sample profile for demonstration."""
        return GitHubProfile(
            username=username,
            name="Sample Developer",
            bio="Passionate developer building impactful software",
            public_repos=25,
            followers=150,
            following=50,
            top_languages=["Python", "JavaScript", "TypeScript"],
            contribution_score=75,
            projects=[
                GitHubProject(
                    name="ai-project",
                    description="Machine learning project",
                    language="Python",
                    stars=45,
                    forks=12,
                    topics=["machine-learning", "python", "ai"],
                    url=f"https://github.com/{username}/ai-project",
                    is_featured=True
                ),
                GitHubProject(
                    name="web-app",
                    description="Full-stack web application",
                    language="TypeScript",
                    stars=23,
                    forks=5,
                    topics=["react", "nodejs", "typescript"],
                    url=f"https://github.com/{username}/web-app",
                    is_featured=True
                )
            ]
        )
    
    def _calculate_contribution_score(self, user: Any, repos: List) -> int:
        """Calculate contribution score based on activity."""
        score = 0
        
        # Base score from repos
        score += min(user.public_repos * 2, 30)
        
        # Score from followers
        score += min(user.followers // 10, 20)
        
        # Score from repo stats
        total_stars = sum(r.stargazers_count for r in repos[:20])
        score += min(total_stars, 30)
        
        # Diversity score
        languages = set(r.language for r in repos if r.language)
        score += min(len(languages) * 2, 20)
        
        return min(score, 100)
    
    def extract_technical_skills(self, profile: GitHubProfile) -> Dict[str, Any]:
        """Extract technical skills from GitHub profile."""
        skills = {
            "programming_languages": profile.top_languages,
            "frameworks": self._detect_frameworks(profile.projects),
            "tools": self._detect_tools(profile.projects),
            "domains": self._detect_domains(profile.projects)
        }
        
        return skills
    
    def _detect_frameworks(self, projects: List[GitHubProject]) -> List[str]:
        """Detect frameworks from project topics and descriptions."""
        frameworks = set()
        framework_keywords = {
            "react": "React",
            "angular": "Angular",
            "vue": "Vue.js",
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "tensorflow": "TensorFlow",
            "pytorch": "PyTorch",
            "express": "Express.js",
            "nextjs": "Next.js",
            "next.js": "Next.js"
        }
        
        for project in projects:
            text = f"{project.description} {' '.join(project.topics)}".lower()
            for keyword, framework in framework_keywords.items():
                if keyword in text:
                    frameworks.add(framework)
        
        return list(frameworks)
    
    def _detect_tools(self, projects: List[GitHubProject]) -> List[str]:
        """Detect tools from project topics."""
        tools = set()
        tool_keywords = {
            "docker": "Docker",
            "kubernetes": "Kubernetes",
            "aws": "AWS",
            "gcp": "Google Cloud",
            "azure": "Azure",
            "terraform": "Terraform",
            "github-actions": "GitHub Actions",
            "ci-cd": "CI/CD"
        }
        
        for project in projects:
            topics = [t.lower() for t in project.topics]
            for keyword, tool in tool_keywords.items():
                if keyword in topics:
                    tools.add(tool)
        
        return list(tools)
    
    def _detect_domains(self, projects: List[GitHubProject]) -> List[str]:
        """Detect domain expertise from projects."""
        domains = set()
        domain_keywords = {
            "machine-learning": "Machine Learning",
            "ml": "Machine Learning",
            "data-science": "Data Science",
            "web": "Web Development",
            "api": "API Development",
            "mobile": "Mobile Development",
            "devops": "DevOps",
            "security": "Security"
        }
        
        for project in projects:
            text = f"{project.description} {' '.join(project.topics)}".lower()
            for keyword, domain in domain_keywords.items():
                if keyword in text:
                    domains.add(domain)
        
        return list(domains)
    
    def format_for_portfolio(
        self, profile: GitHubProfile, max_projects: int = 6
    ) -> List[Dict]:
        """Format GitHub projects for portfolio display."""
        featured_projects = [p for p in profile.projects if p.is_featured]
        other_projects = [p for p in profile.projects if not p.is_featured]
        
        # Prioritize featured projects
        selected = featured_projects[:max_projects]
        remaining_slots = max_projects - len(selected)
        
        if remaining_slots > 0:
            selected.extend(other_projects[:remaining_slots])
        
        return [
            {
                "title": p.name,
                "description": p.description or f"{p.language} project",
                "technologies": [p.language] + p.topics[:3],
                "github_url": p.url,
                "metrics": {
                    "stars": p.stars,
                    "forks": p.forks
                }
            }
            for p in selected
        ]
