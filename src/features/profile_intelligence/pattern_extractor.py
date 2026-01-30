"""
Pattern Extractor Module
Extracts success patterns from top-performing profiles.
"""

from typing import Any, Dict, List, Tuple
from collections import Counter
from dataclasses import dataclass
import re


@dataclass
class ProfilePattern:
    """Represents an extracted pattern."""
    pattern_type: str
    pattern_value: str
    frequency: float
    examples: List[str]
    impact_score: float


class PatternExtractor:
    """
    Extracts and analyzes patterns from successful profiles
    to inform content optimization.
    """
    
    def __init__(self):
        self.pattern_cache: Dict[str, List[ProfilePattern]] = {}
        
    def extract_headline_patterns(
        self, headlines: List[str]
    ) -> Dict[str, Any]:
        """Extract patterns from successful headlines."""
        patterns = {
            "structure": self._analyze_headline_structure(headlines),
            "keywords": self._extract_common_keywords(headlines),
            "length": self._analyze_length_distribution(headlines),
            "formulas": self._identify_headline_formulas(headlines)
        }
        return patterns
    
    def extract_about_patterns(
        self, about_sections: List[str]
    ) -> Dict[str, Any]:
        """Extract patterns from about sections."""
        patterns = {
            "opening_hooks": self._extract_opening_hooks(about_sections),
            "structure": self._analyze_about_structure(about_sections),
            "cta_patterns": self._extract_cta_patterns(about_sections),
            "tone": self._analyze_tone(about_sections)
        }
        return patterns
    
    def extract_experience_patterns(
        self, experiences: List[List[Dict]]
    ) -> Dict[str, Any]:
        """Extract patterns from experience sections."""
        all_bullets = []
        for exp_list in experiences:
            for exp in exp_list:
                bullets = exp.get("bullets", [])
                all_bullets.extend(bullets)
        
        patterns = {
            "action_verbs": self._extract_action_verbs(all_bullets),
            "metrics_usage": self._analyze_metrics_usage(all_bullets),
            "bullet_structure": self._analyze_bullet_structure(all_bullets)
        }
        return patterns
    
    def extract_skill_patterns(
        self, skill_lists: List[List[Dict]]
    ) -> Dict[str, Any]:
        """Extract patterns from skill sections."""
        all_skills = []
        for skills in skill_lists:
            for skill in skills:
                name = skill.get("name", skill) if isinstance(skill, dict) else skill
                all_skills.append(name)
        
        patterns = {
            "top_skills": self._get_top_skills(all_skills),
            "skill_categories": self._categorize_skills(all_skills),
            "endorsement_patterns": self._analyze_endorsements(skill_lists)
        }
        return patterns
    
    def _analyze_headline_structure(self, headlines: List[str]) -> Dict[str, Any]:
        """Analyze structural patterns in headlines."""
        structures = {
            "pipe_separated": 0,
            "bullet_separated": 0,
            "dash_separated": 0,
            "simple": 0
        }
        
        for headline in headlines:
            if "|" in headline:
                structures["pipe_separated"] += 1
            elif "•" in headline:
                structures["bullet_separated"] += 1
            elif " - " in headline:
                structures["dash_separated"] += 1
            else:
                structures["simple"] += 1
        
        total = len(headlines) if headlines else 1
        return {
            k: round(v / total * 100, 1)
            for k, v in structures.items()
        }
    
    def _extract_common_keywords(self, texts: List[str]) -> List[Tuple[str, int]]:
        """Extract most common keywords."""
        words = []
        stop_words = {"the", "a", "an", "and", "or", "in", "at", "for", "to", "of"}
        
        for text in texts:
            text_words = re.findall(r'\b\w+\b', text.lower())
            words.extend([w for w in text_words if w not in stop_words and len(w) > 3])
        
        return Counter(words).most_common(20)
    
    def _analyze_length_distribution(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze length distribution."""
        lengths = [len(t) for t in texts]
        
        if not lengths:
            return {"min": 0, "max": 0, "avg": 0, "optimal_range": (50, 120)}
        
        return {
            "min": min(lengths),
            "max": max(lengths),
            "avg": round(sum(lengths) / len(lengths), 1),
            "optimal_range": (50, 120)
        }
    
    def _identify_headline_formulas(self, headlines: List[str]) -> List[Dict]:
        """Identify common headline formulas."""
        formulas = [
            {
                "name": "Role + Value Prop",
                "pattern": r"^\w+\s+\w+\s*\|.*(?:helping|driving|building)",
                "example": "Software Engineer | Helping teams ship faster",
                "frequency": 0
            },
            {
                "name": "Role + Company + Focus",
                "pattern": r"^\w+.*@.*\|",
                "example": "PM @ Google | Product Strategy",
                "frequency": 0
            },
            {
                "name": "Multiple Expertise Areas",
                "pattern": r".*\|.*\|.*",
                "example": "AI | ML | Data Science",
                "frequency": 0
            }
        ]
        
        for headline in headlines:
            for formula in formulas:
                if re.search(formula["pattern"], headline, re.IGNORECASE):
                    formula["frequency"] += 1
        
        # Calculate percentages
        total = len(headlines) if headlines else 1
        for formula in formulas:
            formula["frequency"] = round(formula["frequency"] / total * 100, 1)
        
        return sorted(formulas, key=lambda x: x["frequency"], reverse=True)
    
    def _extract_opening_hooks(self, about_sections: List[str]) -> List[str]:
        """Extract effective opening hooks."""
        hooks = []
        for about in about_sections:
            first_sentence = about.split(".")[0] if about else ""
            if len(first_sentence) > 10:
                hooks.append(first_sentence[:100])
        return hooks[:10]
    
    def _analyze_about_structure(self, about_sections: List[str]) -> Dict[str, Any]:
        """Analyze structure of about sections."""
        structures = {
            "uses_paragraphs": 0,
            "uses_bullets": 0,
            "has_emoji": 0,
            "has_cta": 0
        }
        
        for about in about_sections:
            if "\n\n" in about:
                structures["uses_paragraphs"] += 1
            if any(c in about for c in ["•", "-", "*"]):
                structures["uses_bullets"] += 1
            if any(ord(c) > 127 for c in about):
                structures["has_emoji"] += 1
            if any(kw in about.lower() for kw in ["reach out", "connect", "contact"]):
                structures["has_cta"] += 1
        
        total = len(about_sections) if about_sections else 1
        return {k: round(v / total * 100, 1) for k, v in structures.items()}
    
    def _extract_cta_patterns(self, about_sections: List[str]) -> List[str]:
        """Extract call-to-action patterns."""
        cta_patterns = []
        cta_keywords = ["reach out", "connect", "contact me", "let's chat", "email me"]
        
        for about in about_sections:
            sentences = about.split(".")
            for sentence in sentences:
                if any(kw in sentence.lower() for kw in cta_keywords):
                    cta_patterns.append(sentence.strip())
        
        return list(set(cta_patterns))[:10]
    
    def _analyze_tone(self, texts: List[str]) -> Dict[str, float]:
        """Analyze writing tone."""
        tones = {"professional": 0, "casual": 0, "technical": 0}
        
        professional_words = {"expertise", "professional", "experience", "strategic"}
        casual_words = {"love", "passionate", "excited", "fun"}
        technical_words = {"implement", "develop", "architecture", "system"}
        
        for text in texts:
            text_lower = text.lower()
            if any(w in text_lower for w in professional_words):
                tones["professional"] += 1
            if any(w in text_lower for w in casual_words):
                tones["casual"] += 1
            if any(w in text_lower for w in technical_words):
                tones["technical"] += 1
        
        total = len(texts) if texts else 1
        return {k: round(v / total * 100, 1) for k, v in tones.items()}
    
    def _extract_action_verbs(self, bullets: List[str]) -> List[Tuple[str, int]]:
        """Extract most common action verbs."""
        verbs = []
        common_action_verbs = {
            "led", "developed", "managed", "created", "implemented",
            "designed", "built", "launched", "improved", "drove",
            "achieved", "increased", "reduced", "established", "spearheaded"
        }
        
        for bullet in bullets:
            words = bullet.lower().split()
            if words:
                first_word = words[0].rstrip(",.:;")
                if first_word in common_action_verbs:
                    verbs.append(first_word)
        
        return Counter(verbs).most_common(15)
    
    def _analyze_metrics_usage(self, bullets: List[str]) -> Dict[str, Any]:
        """Analyze how metrics are used in bullets."""
        metrics_count = 0
        percentage_usage = 0
        dollar_usage = 0
        
        for bullet in bullets:
            if re.search(r'\d+', bullet):
                metrics_count += 1
            if "%" in bullet:
                percentage_usage += 1
            if "$" in bullet:
                dollar_usage += 1
        
        total = len(bullets) if bullets else 1
        return {
            "bullets_with_metrics": round(metrics_count / total * 100, 1),
            "percentage_usage": round(percentage_usage / total * 100, 1),
            "dollar_usage": round(dollar_usage / total * 100, 1)
        }
    
    def _analyze_bullet_structure(self, bullets: List[str]) -> Dict[str, Any]:
        """Analyze structure of bullet points."""
        lengths = [len(b) for b in bullets]
        
        return {
            "avg_length": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "optimal_length": (50, 150),
            "starts_with_verb": self._count_verb_starters(bullets)
        }
    
    def _count_verb_starters(self, bullets: List[str]) -> float:
        """Count percentage of bullets starting with verbs."""
        action_verbs = {"led", "developed", "managed", "created", "built", "achieved"}
        count = 0
        
        for bullet in bullets:
            words = bullet.lower().split()
            if words and words[0] in action_verbs:
                count += 1
        
        total = len(bullets) if bullets else 1
        return round(count / total * 100, 1)
    
    def _get_top_skills(self, skills: List[str]) -> List[Tuple[str, int]]:
        """Get most common skills."""
        return Counter(skills).most_common(20)
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, int]:
        """Categorize skills into groups."""
        categories = {"technical": 0, "soft": 0, "tools": 0, "domain": 0}
        
        technical = {"python", "java", "sql", "aws", "machine learning"}
        soft = {"leadership", "communication", "teamwork", "problem solving"}
        tools = {"excel", "tableau", "jira", "git", "docker"}
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(t in skill_lower for t in technical):
                categories["technical"] += 1
            elif any(t in skill_lower for t in soft):
                categories["soft"] += 1
            elif any(t in skill_lower for t in tools):
                categories["tools"] += 1
            else:
                categories["domain"] += 1
        
        return categories
    
    def _analyze_endorsements(self, skill_lists: List[List[Dict]]) -> Dict[str, Any]:
        """Analyze endorsement patterns."""
        endorsements = []
        
        for skills in skill_lists:
            for skill in skills:
                if isinstance(skill, dict):
                    endorsements.append(skill.get("endorsements", 0))
        
        if not endorsements:
            return {"avg": 0, "max": 0, "min": 0}
        
        return {
            "avg": round(sum(endorsements) / len(endorsements), 1),
            "max": max(endorsements),
            "min": min(endorsements)
        }
