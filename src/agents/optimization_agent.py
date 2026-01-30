"""
Optimization Agent
Handles continuous learning and adaptation based on feedback signals.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from loguru import logger

from .base_agent import BaseAgent, AgentAction


class OptimizationAgent(BaseAgent):
    """
    Agent responsible for continuous optimization based on
    feedback signals and market trends.
    """
    
    def __init__(self, llm_client: Any = None):
        super().__init__(
            name="OptimizationAgent",
            description="Optimizes content based on feedback",
            llm_client=llm_client
        )
        self.optimization_history: List[Dict] = []
        
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback and decide optimization actions."""
        feedback = input_data.get("feedback", {})
        current_content = input_data.get("current_content", {})
        market_trends = input_data.get("market_trends", {})
        
        # Analyze what needs optimization
        analysis = self._analyze_feedback(feedback)
        
        actions = []
        
        if analysis.get("headline_needs_update"):
            actions.append({
                "name": "optimize_headline",
                "input": {
                    "current": current_content.get("headline"),
                    "feedback": feedback.get("headline_metrics", {}),
                    "trends": market_trends.get("headline_trends", {})
                }
            })
            
        if analysis.get("skills_need_reorder"):
            actions.append({
                "name": "reorder_skills",
                "input": {
                    "current_skills": current_content.get("skills", []),
                    "market_demand": market_trends.get("skill_demand", {}),
                    "engagement": feedback.get("skill_engagement", {})
                }
            })
            
        if analysis.get("portfolio_needs_update"):
            actions.append({
                "name": "update_portfolio",
                "input": {
                    "current_layout": current_content.get("portfolio_layout"),
                    "engagement_metrics": feedback.get("portfolio_metrics", {}),
                    "trends": market_trends.get("portfolio_trends", {})
                }
            })
        
        return {
            "actions": actions,
            "analysis": analysis,
            "strategy": "continuous_optimization"
        }
    
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute optimization actions."""
        action_map = {
            "optimize_headline": self._optimize_headline,
            "reorder_skills": self._reorder_skills,
            "update_portfolio": self._update_portfolio,
            "generate_ab_test": self._generate_ab_test,
        }
        
        handler = action_map.get(action.name)
        if handler:
            result = await handler(action.input_data)
            self._record_optimization(action.name, result)
            return result
        
        return {"error": f"Unknown action: {action.name}"}
    
    def _analyze_feedback(self, feedback: Dict) -> Dict[str, bool]:
        """Analyze feedback to determine what needs optimization."""
        analysis = {
            "headline_needs_update": False,
            "skills_need_reorder": False,
            "portfolio_needs_update": False,
            "content_needs_refresh": False
        }
        
        # Check profile view trends
        view_trend = feedback.get("profile_views_trend", 0)
        if view_trend < 0:  # Declining views
            analysis["headline_needs_update"] = True
            analysis["content_needs_refresh"] = True
        
        # Check skill engagement
        skill_clicks = feedback.get("skill_click_rate", 0)
        if skill_clicks < 0.05:  # Less than 5% click rate
            analysis["skills_need_reorder"] = True
        
        # Check portfolio metrics
        bounce_rate = feedback.get("portfolio_bounce_rate", 0)
        if bounce_rate > 0.7:  # More than 70% bounce
            analysis["portfolio_needs_update"] = True
        
        return analysis
    
    async def _optimize_headline(self, data: Dict) -> Dict[str, Any]:
        """Optimize headline based on feedback."""
        current = data.get("current", "")
        feedback = data.get("feedback", {})
        trends = data.get("trends", {})
        
        # Generate optimization suggestions
        suggestions = self._generate_headline_suggestions(current, feedback, trends)
        
        # Score and rank suggestions
        ranked = self._rank_suggestions(suggestions, feedback)
        
        return {
            "optimization_type": "headline",
            "current": current,
            "suggestions": ranked,
            "recommended": ranked[0] if ranked else current,
            "confidence": self._calculate_confidence(feedback)
        }
    
    async def _reorder_skills(self, data: Dict) -> Dict[str, Any]:
        """Reorder skills based on market demand and engagement."""
        current_skills = data.get("current_skills", [])
        market_demand = data.get("market_demand", {})
        engagement = data.get("engagement", {})
        
        # Score each skill
        scored_skills = []
        for skill in current_skills:
            name = skill if isinstance(skill, str) else skill.get("name", "")
            score = self._calculate_skill_score(name, market_demand, engagement)
            scored_skills.append({"name": name, "score": score})
        
        # Sort by score
        sorted_skills = sorted(scored_skills, key=lambda x: x["score"], reverse=True)
        
        return {
            "optimization_type": "skills",
            "original_order": current_skills,
            "optimized_order": [s["name"] for s in sorted_skills],
            "scores": {s["name"]: s["score"] for s in sorted_skills}
        }
    
    async def _update_portfolio(self, data: Dict) -> Dict[str, Any]:
        """Update portfolio layout based on engagement metrics."""
        current_layout = data.get("current_layout", {})
        metrics = data.get("engagement_metrics", {})
        trends = data.get("trends", {})
        
        # Analyze section performance
        section_performance = self._analyze_section_performance(metrics)
        
        # Generate layout recommendations
        recommendations = self._generate_layout_recommendations(
            current_layout, section_performance, trends
        )
        
        return {
            "optimization_type": "portfolio",
            "current_layout": current_layout,
            "section_performance": section_performance,
            "recommendations": recommendations
        }
    
    async def _generate_ab_test(self, data: Dict) -> Dict[str, Any]:
        """Generate A/B test variants."""
        content_type = data.get("content_type", "headline")
        current = data.get("current", "")
        
        variants = []
        if content_type == "headline":
            variants = self._generate_headline_variants(current)
        
        return {
            "test_type": f"{content_type}_ab_test",
            "control": current,
            "variants": variants,
            "recommended_duration": "7 days"
        }
    
    def _generate_headline_suggestions(
        self, current: str, feedback: Dict, trends: Dict
    ) -> List[str]:
        """Generate headline improvement suggestions."""
        suggestions = []
        
        # Add trending keywords
        trending_keywords = trends.get("keywords", [])
        if trending_keywords:
            for kw in trending_keywords[:3]:
                if kw.lower() not in current.lower():
                    suggestions.append(f"{current} | {kw}")
        
        # Add metric-based improvements
        if feedback.get("search_appearances", 0) < 10:
            suggestions.append(current.replace("|", "•"))
        
        return suggestions if suggestions else [current]
    
    def _rank_suggestions(self, suggestions: List[str], feedback: Dict) -> List[str]:
        """Rank suggestions by expected performance."""
        # Simple ranking based on length and keyword presence
        scored = []
        for s in suggestions:
            score = 50
            if len(s) <= 120:
                score += 20
            if "|" in s or "•" in s:
                score += 15
            scored.append((s, score))
        
        return [s[0] for s in sorted(scored, key=lambda x: x[1], reverse=True)]
    
    def _calculate_skill_score(
        self, skill: str, market_demand: Dict, engagement: Dict
    ) -> float:
        """Calculate optimization score for a skill."""
        demand_score = market_demand.get(skill.lower(), 50)
        engagement_score = engagement.get(skill.lower(), 50)
        return (demand_score * 0.6) + (engagement_score * 0.4)
    
    def _analyze_section_performance(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze performance of each portfolio section."""
        return {
            "hero": {"scroll_depth": 100, "time_spent": metrics.get("hero_time", 5)},
            "projects": {"scroll_depth": 80, "engagement": metrics.get("project_clicks", 0)},
            "skills": {"scroll_depth": 70, "engagement": metrics.get("skill_views", 0)},
            "contact": {"scroll_depth": 40, "conversions": metrics.get("contact_clicks", 0)}
        }
    
    def _generate_layout_recommendations(
        self, current: Dict, performance: Dict, trends: Dict
    ) -> List[Dict]:
        """Generate layout improvement recommendations."""
        recommendations = []
        
        if performance.get("projects", {}).get("scroll_depth", 0) < 50:
            recommendations.append({
                "type": "reorder",
                "action": "Move projects section higher",
                "reason": "Low scroll depth for projects section"
            })
        
        if performance.get("contact", {}).get("conversions", 0) < 1:
            recommendations.append({
                "type": "enhance",
                "action": "Add floating CTA button",
                "reason": "Low contact conversions"
            })
        
        return recommendations
    
    def _generate_headline_variants(self, current: str) -> List[str]:
        """Generate headline variants for A/B testing."""
        variants = []
        
        # Variant 1: Add emoji
        variants.append(f"🚀 {current}")
        
        # Variant 2: Different separator
        if "|" in current:
            variants.append(current.replace("|", "•"))
        
        # Variant 3: Shorter version
        words = current.split()
        if len(words) > 6:
            variants.append(" ".join(words[:6]))
        
        return variants
    
    def _calculate_confidence(self, feedback: Dict) -> float:
        """Calculate confidence score for recommendations."""
        data_points = sum([
            feedback.get("profile_views", 0) > 0,
            feedback.get("search_appearances", 0) > 0,
            feedback.get("connection_requests", 0) > 0,
        ])
        return min(data_points * 0.33, 1.0)
    
    def _record_optimization(self, action: str, result: Dict):
        """Record optimization for tracking."""
        self.optimization_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result_summary": result.get("optimization_type", "unknown")
        })
