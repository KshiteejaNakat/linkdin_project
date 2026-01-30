"""
Metrics Collector Module
Collects and tracks career performance metrics.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from loguru import logger


@dataclass
class ProfileMetrics:
    """LinkedIn profile metrics."""
    profile_views: int = 0
    search_appearances: int = 0
    post_impressions: int = 0
    connection_requests: int = 0
    recruiter_messages: int = 0
    profile_strength: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PortfolioMetrics:
    """Portfolio website metrics."""
    page_views: int = 0
    unique_visitors: int = 0
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    contact_clicks: int = 0
    project_clicks: int = 0
    resume_downloads: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CareerMetrics:
    """Overall career outcome metrics."""
    job_applications: int = 0
    interviews_scheduled: int = 0
    offers_received: int = 0
    interview_conversion_rate: float = 0.0
    response_rate: float = 0.0


class MetricsCollector:
    """
    Collects and manages career performance metrics
    for continuous optimization.
    """
    
    def __init__(self):
        self.profile_history: List[ProfileMetrics] = []
        self.portfolio_history: List[PortfolioMetrics] = []
        self.career_metrics = CareerMetrics()
        
    def record_profile_metrics(self, metrics: Dict[str, Any]) -> ProfileMetrics:
        """Record LinkedIn profile metrics."""
        profile_metrics = ProfileMetrics(
            profile_views=metrics.get("profile_views", 0),
            search_appearances=metrics.get("search_appearances", 0),
            post_impressions=metrics.get("post_impressions", 0),
            connection_requests=metrics.get("connection_requests", 0),
            recruiter_messages=metrics.get("recruiter_messages", 0),
            profile_strength=metrics.get("profile_strength", 0),
            timestamp=datetime.now()
        )
        
        self.profile_history.append(profile_metrics)
        logger.info(f"Recorded profile metrics: {profile_metrics.profile_views} views")
        
        return profile_metrics
    
    def record_portfolio_metrics(self, metrics: Dict[str, Any]) -> PortfolioMetrics:
        """Record portfolio website metrics."""
        portfolio_metrics = PortfolioMetrics(
            page_views=metrics.get("page_views", 0),
            unique_visitors=metrics.get("unique_visitors", 0),
            avg_time_on_page=metrics.get("avg_time_on_page", 0.0),
            bounce_rate=metrics.get("bounce_rate", 0.0),
            contact_clicks=metrics.get("contact_clicks", 0),
            project_clicks=metrics.get("project_clicks", 0),
            resume_downloads=metrics.get("resume_downloads", 0),
            timestamp=datetime.now()
        )
        
        self.portfolio_history.append(portfolio_metrics)
        logger.info(f"Recorded portfolio metrics: {portfolio_metrics.page_views} views")
        
        return portfolio_metrics
    
    def update_career_metrics(self, metrics: Dict[str, Any]) -> CareerMetrics:
        """Update career outcome metrics."""
        self.career_metrics.job_applications += metrics.get("new_applications", 0)
        self.career_metrics.interviews_scheduled += metrics.get("new_interviews", 0)
        self.career_metrics.offers_received += metrics.get("new_offers", 0)
        
        # Calculate rates
        if self.career_metrics.job_applications > 0:
            self.career_metrics.interview_conversion_rate = (
                self.career_metrics.interviews_scheduled / 
                self.career_metrics.job_applications * 100
            )
        
        if self.career_metrics.interviews_scheduled > 0:
            self.career_metrics.response_rate = (
                self.career_metrics.offers_received /
                self.career_metrics.interviews_scheduled * 100
            )
        
        return self.career_metrics
    
    def get_profile_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get profile metric trends."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [m for m in self.profile_history if m.timestamp > cutoff]
        
        if len(recent) < 2:
            return {"trend": "insufficient_data", "data_points": len(recent)}
        
        # Calculate trends
        first_half = recent[:len(recent)//2]
        second_half = recent[len(recent)//2:]
        
        first_avg_views = sum(m.profile_views for m in first_half) / len(first_half)
        second_avg_views = sum(m.profile_views for m in second_half) / len(second_half)
        
        view_trend = ((second_avg_views - first_avg_views) / first_avg_views * 100
                      if first_avg_views > 0 else 0)
        
        return {
            "profile_views_trend": round(view_trend, 1),
            "total_views": sum(m.profile_views for m in recent),
            "avg_daily_views": sum(m.profile_views for m in recent) / days,
            "data_points": len(recent),
            "period_days": days
        }
    
    def get_portfolio_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get portfolio metric trends."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [m for m in self.portfolio_history if m.timestamp > cutoff]
        
        if not recent:
            return {"trend": "no_data"}
        
        total_views = sum(m.page_views for m in recent)
        avg_bounce = sum(m.bounce_rate for m in recent) / len(recent)
        total_contacts = sum(m.contact_clicks for m in recent)
        
        return {
            "total_page_views": total_views,
            "avg_bounce_rate": round(avg_bounce, 2),
            "total_contact_clicks": total_contacts,
            "conversion_rate": (total_contacts / total_views * 100 
                               if total_views > 0 else 0),
            "data_points": len(recent)
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary."""
        profile_trends = self.get_profile_trends()
        portfolio_trends = self.get_portfolio_trends()
        
        return {
            "profile": {
                "trends": profile_trends,
                "latest": self.profile_history[-1].__dict__ if self.profile_history else None
            },
            "portfolio": {
                "trends": portfolio_trends,
                "latest": self.portfolio_history[-1].__dict__ if self.portfolio_history else None
            },
            "career": {
                "applications": self.career_metrics.job_applications,
                "interviews": self.career_metrics.interviews_scheduled,
                "offers": self.career_metrics.offers_received,
                "interview_rate": round(self.career_metrics.interview_conversion_rate, 1),
                "offer_rate": round(self.career_metrics.response_rate, 1)
            }
        }
    
    def identify_improvement_areas(self) -> List[Dict[str, Any]]:
        """Identify areas needing improvement."""
        improvements = []
        
        # Check profile trends
        profile_trends = self.get_profile_trends()
        if profile_trends.get("profile_views_trend", 0) < 0:
            improvements.append({
                "area": "profile_visibility",
                "issue": "Profile views declining",
                "severity": "high",
                "suggestion": "Update headline and add trending keywords"
            })
        
        # Check portfolio bounce rate
        portfolio_trends = self.get_portfolio_trends()
        if portfolio_trends.get("avg_bounce_rate", 0) > 0.7:
            improvements.append({
                "area": "portfolio_engagement",
                "issue": "High bounce rate on portfolio",
                "severity": "medium",
                "suggestion": "Improve hero section and add clear CTAs"
            })
        
        # Check conversion
        if portfolio_trends.get("conversion_rate", 0) < 2:
            improvements.append({
                "area": "conversion",
                "issue": "Low contact conversion rate",
                "severity": "medium",
                "suggestion": "Make contact information more prominent"
            })
        
        # Check interview rate
        if self.career_metrics.interview_conversion_rate < 10:
            improvements.append({
                "area": "applications",
                "issue": "Low interview conversion rate",
                "severity": "high",
                "suggestion": "Tailor resume and applications more specifically"
            })
        
        return improvements
    
    def export_metrics(self, format: str = "json") -> str:
        """Export metrics data."""
        import json
        
        data = {
            "profile_history": [
                {**m.__dict__, "timestamp": m.timestamp.isoformat()}
                for m in self.profile_history
            ],
            "portfolio_history": [
                {**m.__dict__, "timestamp": m.timestamp.isoformat()}
                for m in self.portfolio_history
            ],
            "career_metrics": self.career_metrics.__dict__,
            "summary": self.get_performance_summary()
        }
        
        return json.dumps(data, indent=2, default=str)
