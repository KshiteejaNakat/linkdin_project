"""
Helper Functions Module
Common utility functions used across the application.
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'"()@#$%&*]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text


def extract_keywords(
    text: str,
    min_length: int = 3,
    max_keywords: int = 20
) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        max_keywords: Maximum number of keywords
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'is', 'in', 'to', 'of', 'for', 'with',
        'on', 'at', 'by', 'from', 'as', 'an', 'be', 'was',
        'are', 'been', 'being', 'have', 'has', 'had', 'do',
        'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'shall', 'can', 'need', 'our',
        'you', 'your', 'they', 'them', 'their', 'this', 'that',
        'these', 'those', 'which', 'who', 'whom', 'whose'
    }
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter and count
    filtered = [
        w for w in words
        if len(w) >= min_length and w not in stop_words
    ]
    
    # Get most common
    counter = Counter(filtered)
    keywords = [word for word, _ in counter.most_common(max_keywords)]
    
    return keywords


def calculate_score(
    metrics: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate weighted score from metrics.
    
    Args:
        metrics: Dict of metric name to value
        weights: Optional weights for each metric
        
    Returns:
        Weighted average score
    """
    if not metrics:
        return 0.0
    
    if weights is None:
        weights = {k: 1.0 for k in metrics}
    
    total_weight = sum(weights.get(k, 1.0) for k in metrics)
    
    if total_weight == 0:
        return 0.0
    
    weighted_sum = sum(
        v * weights.get(k, 1.0)
        for k, v in metrics.items()
    )
    
    return weighted_sum / total_weight


def format_duration(start_date: str, end_date: Optional[str] = None) -> str:
    """
    Format date range as human-readable duration.
    
    Args:
        start_date: Start date string
        end_date: End date string or None for present
        
    Returns:
        Formatted duration string
    """
    try:
        start = parse_date(start_date)
        end = parse_date(end_date) if end_date else datetime.now()
        
        months = (end.year - start.year) * 12 + (end.month - start.month)
        years = months // 12
        remaining_months = months % 12
        
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years > 1 else ''}")
        if remaining_months > 0:
            parts.append(f"{remaining_months} month{'s' if remaining_months > 1 else ''}")
        
        return " ".join(parts) if parts else "Less than a month"
    except Exception:
        return "Duration unavailable"


def parse_date(date_str: str) -> datetime:
    """Parse date string in various formats."""
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%B %Y",
        "%b %Y",
        "%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text or ""
    
    return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix


def generate_id(prefix: str = "") -> str:
    """Generate unique identifier."""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge multiple dictionaries."""
    result = {}
    
    for d in dicts:
        if not d:
            continue
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
    
    return result
