"""
Adaptation Engine Module
Generates optimization recommendations based on metrics.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger


@dataclass
class Recommendation:
    """Optimization recommendation."""
    id: str
    category: str
    priority: str  # high, medium, low
    title: str
    description: str
    action: str
    auto_applicable: bool
    expected_impact: str
    created_at: datetime


class AdaptationEngine:
    """
    Analyzes metrics and generates optimization recommendations
    for continuous career improvement.
    """
    
    def __init__(self):
        self.recommendation_history: List[Recommendation] = []
        self.applied_recommendations: List[str] = []
        
    def analyze_and_recommend(
        self,
        metrics_summary: Dict[str, Any],
        current_content: Dict[str, Any],
        market_trends: Optional[Dict] = None
    ) -> List[Recommendation]:
        """Generate recommendations based on metrics analysis."""
        recommendations = []
        
        # Analyze profile metrics
        profile_recs = self._analyze_profile_metrics(
            metrics_summary.get("profile", {}),
            current_content,
            market_trends
        )
        recommendations.extend(profile_recs)
        
        # Analyze portfolio metrics
        portfolio_recs = self._analyze_portfolio_metrics(
            metrics_summary.get("portfolio", {}),
            current_content
        )
        recommendations.extend(portfolio_recs)
        
        # Analyze career metrics
        career_recs = self._analyze_career_metrics(
            metrics_summary.get("career", {})
        )
        recommendations.extend(career_recs)
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x.priority, 2))
        
        # Store recommendations
        self.recommendation_history.extend(recommendations)
        
        return recommendations
    
    def _analyze_profile_metrics(
        self,
        profile_data: Dict,
        content: Dict,
        trends: Optional[Dict]
    ) -> List[Recommendation]:
        """Analyze profile metrics and generate recommendations."""
        recommendations = []
        
        trends_data = profile_data.get("trends", {})
        latest = profile_data.get("latest", {})
        
        # Check view trends
        view_trend = trends_data.get("profile_views_trend", 0)
        
        if view_trend < -10:
            recommendations.append(Recommendation(
                id=f"profile_{datetime.now().timestamp()}",
                category="profile",
                priority="high",
                title="Profile Visibility Declining",
                description="Your profile views have decreased significantly. "
                           "This may indicate your headline needs updating.",
                action="update_headline",
                auto_applicable=False,
                expected_impact="15-30% increase in profile views",
                created_at=datetime.now()
            ))
        
        # Check search appearances
        search_appearances = latest.get("search_appearances", 0)
        if search_appearances < 10:
            recommendations.append(Recommendation(
                id=f"seo_{datetime.now().timestamp()}",
                category="profile",
                priority="medium",
                title="Low Search Visibility",
                description="You're not appearing in many searches. "
                           "Consider adding more relevant keywords to your profile.",
                action="add_keywords",
                auto_applicable=False,
                expected_impact="Increase search appearances by 50%",
                created_at=datetime.now()
            ))
        
        # Check recruiter messages
        recruiter_msgs = latest.get("recruiter_messages", 0)
        if recruiter_msgs == 0 and search_appearances > 20:
            recommendations.append(Recommendation(
                id=f"recruiter_{datetime.now().timestamp()}",
                category="profile",
                priority="medium",
                title="No Recruiter Engagement",
                description="You're visible but not getting recruiter messages. "
                           "Your About section may need strengthening.",
                action="enhance_about",
                auto_applicable=False,
                expected_impact="Start receiving recruiter outreach",
                created_at=datetime.now()
            ))
        
        # Market trend alignment
        if trends:
            trending_skills = trends.get("emerging_skills", [])
            current_skills = content.get("skills", [])
            
            missing_trending = [
                s["skill"] for s in trending_skills 
                if s["skill"].lower() not in [c.lower() for c in current_skills]
            ]
            
            if missing_trending:
                recommendations.append(Recommendation(
                    id=f"skills_{datetime.now().timestamp()}",
                    category="skills",
                    priority="medium",
                    title="Trending Skills Gap",
                    description=f"Consider adding trending skills: {', '.join(missing_trending[:3])}",
                    action="add_skills",
                    auto_applicable=False,
                    expected_impact="Better alignment with market demand",
                    created_at=datetime.now()
                ))
        
        return recommendations
    
    def _analyze_portfolio_metrics(
        self,
        portfolio_data: Dict,
        content: Dict
    ) -> List[Recommendation]:
        """Analyze portfolio metrics and generate recommendations."""
        recommendations = []
        
        trends = portfolio_data.get("trends", {})
        
        # Check bounce rate
        bounce_rate = trends.get("avg_bounce_rate", 0)
        if bounce_rate > 0.7:
            recommendations.append(Recommendation(
                id=f"bounce_{datetime.now().timestamp()}",
                category="portfolio",
                priority="high",
                title="High Bounce Rate",
                description="70%+ of visitors leave quickly. "
                           "Your hero section needs to be more engaging.",
                action="improve_hero",
                auto_applicable=True,
                expected_impact="Reduce bounce rate by 20-30%",
                created_at=datetime.now()
            ))
        
        # Check conversion rate
        conversion = trends.get("conversion_rate", 0)
        if conversion < 2:
            recommendations.append(Recommendation(
                id=f"cta_{datetime.now().timestamp()}",
                category="portfolio",
                priority="medium",
                title="Low Conversion Rate",
                description="Few visitors are contacting you. "
                           "Add more prominent call-to-action buttons.",
                action="add_cta",
                auto_applicable=True,
                expected_impact="Double your contact rate",
                created_at=datetime.now()
            ))
        
        # Check project engagement
        project_clicks = trends.get("total_project_clicks", 0)
        total_views = trends.get("total_page_views", 1)
        
        if project_clicks / total_views < 0.1:
            recommendations.append(Recommendation(
                id=f"projects_{datetime.now().timestamp()}",
                category="portfolio",
                priority="low",
                title="Low Project Engagement",
                description="Visitors aren't exploring your projects. "
                           "Consider adding better project previews.",
                action="enhance_projects",
                auto_applicable=False,
                expected_impact="Increase project exploration by 50%",
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def _analyze_career_metrics(
        self,
        career_data: Dict
    ) -> List[Recommendation]:
        """Analyze career metrics and generate recommendations."""
        recommendations = []
        
        interview_rate = career_data.get("interview_rate", 0)
        offer_rate = career_data.get("offer_rate", 0)
        
        if interview_rate < 10:
            recommendations.append(Recommendation(
                id=f"interview_{datetime.now().timestamp()}",
                category="career",
                priority="high",
                title="Low Interview Rate",
                description="Less than 10% of applications lead to interviews. "
                           "Your resume may not be aligned with job requirements.",
                action="tailor_resume",
                auto_applicable=False,
                expected_impact="Increase interview rate to 15-20%",
                created_at=datetime.now()
            ))
        
        if offer_rate < 20 and interview_rate > 10:
            recommendations.append(Recommendation(
                id=f"interview_prep_{datetime.now().timestamp()}",
                category="career",
                priority="medium",
                title="Interview Conversion Gap",
                description="You're getting interviews but not offers. "
                           "Focus on interview preparation and storytelling.",
                action="interview_coaching",
                auto_applicable=False,
                expected_impact="Improve offer rate to 30%+",
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def get_action_plan(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
        """Generate actionable plan from recommendations."""
        high_priority = [r for r in recommendations if r.priority == "high"]
        medium_priority = [r for r in recommendations if r.priority == "medium"]
        low_priority = [r for r in recommendations if r.priority == "low"]
        
        auto_actions = [r for r in recommendations if r.auto_applicable]
        manual_actions = [r for r in recommendations if not r.auto_applicable]
        
        return {
            "summary": {
                "total_recommendations": len(recommendations),
                "high_priority": len(high_priority),
                "auto_applicable": len(auto_actions)
            },
            "immediate_actions": [
                {"title": r.title, "action": r.action}
                for r in high_priority[:3]
            ],
            "auto_apply": [
                {"id": r.id, "action": r.action, "title": r.title}
                for r in auto_actions
            ],
            "requires_approval": [
                {"id": r.id, "action": r.action, "title": r.title}
                for r in manual_actions
            ],
            "timeline": {
                "week_1": [r.title for r in high_priority],
                "week_2": [r.title for r in medium_priority],
                "week_3": [r.title for r in low_priority]
            }
        }
    
    def apply_recommendation(self, recommendation_id: str) -> Dict[str, Any]:
        """Mark recommendation as applied."""
        self.applied_recommendations.append(recommendation_id)
        
        return {
            "status": "applied",
            "recommendation_id": recommendation_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_recommendation_history(self) -> List[Dict]:
        """Get history of all recommendations."""
        return [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category,
                "priority": r.priority,
                "applied": r.id in self.applied_recommendations,
                "created_at": r.created_at.isoformat()
            }
            for r in self.recommendation_history
        ]
