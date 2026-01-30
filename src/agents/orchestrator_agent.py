"""
Orchestrator Agent
Coordinates all other agents to achieve career optimization goals.
"""

from typing import Any, Dict, List, Optional
from loguru import logger

from .base_agent import BaseAgent, AgentAction, AgentMessage
from .profile_analyzer_agent import ProfileAnalyzerAgent
from .content_generator_agent import ContentGeneratorAgent
from .portfolio_agent import PortfolioAgent
from .optimization_agent import OptimizationAgent


class OrchestratorAgent(BaseAgent):
    """
    Master agent that coordinates all specialized agents
    to achieve comprehensive career optimization.
    """
    
    def __init__(self, llm_client: Any = None):
        super().__init__(
            name="Orchestrator",
            description="Coordinates all career optimization agents",
            llm_client=llm_client
        )
        
        # Initialize sub-agents
        self.profile_analyzer = ProfileAnalyzerAgent(llm_client)
        self.content_generator = ContentGeneratorAgent(llm_client)
        self.portfolio_builder = PortfolioAgent(llm_client)
        self.optimization_agent = OptimizationAgent(llm_client)
        
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine the workflow based on user request.
        """
        request_type = input_data.get("request_type", "full_optimization")
        
        workflows = {
            "full_optimization": [
                "analyze_profile", "build_career_dna", 
                "generate_content", "build_portfolio"
            ],
            "profile_only": ["analyze_profile", "generate_content"],
            "portfolio_only": ["build_career_dna", "build_portfolio"],
            "optimize": ["analyze_feedback", "apply_optimizations"],
        }
        
        workflow = workflows.get(request_type, workflows["full_optimization"])
        
        actions = [{"name": step, "input": input_data} for step in workflow]
        
        return {
            "actions": actions,
            "workflow": workflow,
            "strategy": request_type
        }
    
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute orchestrated actions."""
        action_map = {
            "analyze_profile": self._run_profile_analysis,
            "build_career_dna": self._build_career_dna,
            "generate_content": self._generate_content,
            "build_portfolio": self._build_portfolio,
            "analyze_feedback": self._analyze_feedback,
            "apply_optimizations": self._apply_optimizations,
        }
        
        handler = action_map.get(action.name)
        if handler:
            return await handler(action.input_data)
        
        return {"error": f"Unknown action: {action.name}"}
    
    async def _run_profile_analysis(self, data: Dict) -> Dict[str, Any]:
        """Run profile analysis through analyzer agent."""
        logger.info("Running profile analysis...")
        
        result = await self.profile_analyzer.run({
            "profile_data": data.get("profile_data", {}),
            "analysis_type": "full"
        })
        
        return {
            "step": "profile_analysis",
            "result": result
        }
    
    async def _build_career_dna(self, data: Dict) -> Dict[str, Any]:
        """Build career DNA from user data."""
        logger.info("Building career DNA...")
        
        user_data = data.get("user_data", {})
        profile_analysis = data.get("profile_analysis", {})
        
        career_dna = {
            "strengths": self._extract_strengths(user_data, profile_analysis),
            "gaps": self._identify_gaps(user_data, profile_analysis),
            "opportunities": self._find_opportunities(user_data),
            "recommended_focus": self._determine_focus(user_data)
        }
        
        return {
            "step": "career_dna",
            "result": career_dna
        }
    
    async def _generate_content(self, data: Dict) -> Dict[str, Any]:
        """Generate optimized content through content agent."""
        logger.info("Generating optimized content...")
        
        result = await self.content_generator.run({
            "content_type": "all",
            "user_data": data.get("user_data", {}),
            "market_patterns": data.get("market_patterns", {})
        })
        
        return {
            "step": "content_generation",
            "result": result
        }
    
    async def _build_portfolio(self, data: Dict) -> Dict[str, Any]:
        """Build portfolio through portfolio agent."""
        logger.info("Building portfolio...")
        
        result = await self.portfolio_builder.run({
            "user_data": data.get("user_data", {}),
            "career_dna": data.get("career_dna", {})
        })
        
        return {
            "step": "portfolio_building",
            "result": result
        }
    
    async def _analyze_feedback(self, data: Dict) -> Dict[str, Any]:
        """Analyze feedback for optimization opportunities."""
        logger.info("Analyzing feedback...")
        
        result = await self.optimization_agent.run({
            "feedback": data.get("feedback", {}),
            "current_content": data.get("current_content", {}),
            "market_trends": data.get("market_trends", {})
        })
        
        return {
            "step": "feedback_analysis",
            "result": result
        }
    
    async def _apply_optimizations(self, data: Dict) -> Dict[str, Any]:
        """Apply recommended optimizations."""
        logger.info("Applying optimizations...")
        
        optimizations = data.get("optimizations", [])
        applied = []
        
        for opt in optimizations:
            if opt.get("auto_apply", False):
                applied.append(opt)
        
        return {
            "step": "apply_optimizations",
            "applied": applied,
            "pending_approval": [o for o in optimizations if not o.get("auto_apply")]
        }
    
    def _extract_strengths(self, user_data: Dict, analysis: Dict) -> List[str]:
        """Extract user's key strengths."""
        strengths = []
        
        # From skills with high proficiency
        skills = user_data.get("skills", [])
        for skill in skills[:5]:
            name = skill.get("name", skill) if isinstance(skill, dict) else skill
            strengths.append(name)
        
        return strengths
    
    def _identify_gaps(self, user_data: Dict, analysis: Dict) -> List[str]:
        """Identify gaps vs top performers."""
        gaps = []
        
        results = analysis.get("results", [])
        for result in results:
            if isinstance(result, dict):
                recs = result.get("recommendations", [])
                gaps.extend(recs)
        
        return gaps[:5]
    
    def _find_opportunities(self, user_data: Dict) -> List[str]:
        """Find career growth opportunities."""
        target_role = user_data.get("target_role", "")
        current_role = user_data.get("current_role", "")
        
        opportunities = []
        if target_role != current_role:
            opportunities.append(f"Transition to {target_role}")
        
        return opportunities
    
    def _determine_focus(self, user_data: Dict) -> List[str]:
        """Determine recommended focus areas."""
        return [
            "Optimize LinkedIn headline",
            "Enhance project descriptions",
            "Build thought leadership content"
        ]
