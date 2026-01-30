"""
Base Agent Module
Provides the foundational agent class for all specialized agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class AgentState(Enum):
    """Agent execution states."""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Message structure for agent communication."""
    role: str  # "user", "agent", "system"
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    

@dataclass
class AgentAction:
    """Represents an action taken by an agent."""
    name: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: str = "pending"
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Base class for all AI agents in the Career Architect system.
    Implements the core agent loop and communication patterns.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        llm_client: Any = None
    ):
        self.name = name
        self.description = description
        self.llm_client = llm_client
        self.state = AgentState.IDLE
        self.memory: List[AgentMessage] = []
        self.actions_history: List[AgentAction] = []
        
    @abstractmethod
    async def think(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and decide on actions.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    async def execute(self, action: AgentAction) -> Dict[str, Any]:
        """
        Execute a decided action.
        Must be implemented by subclasses.
        """
        pass
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent loop: Think -> Execute -> Reflect.
        """
        try:
            self.state = AgentState.THINKING
            logger.info(f"[{self.name}] Starting thought process...")
            
            # Think phase
            thought_result = await self.think(input_data)
            
            # Execute phase
            self.state = AgentState.EXECUTING
            actions = thought_result.get("actions", [])
            results = []
            
            for action_data in actions:
                action = AgentAction(
                    name=action_data["name"],
                    input_data=action_data.get("input", {})
                )
                result = await self.execute(action)
                action.output_data = result
                action.status = "completed"
                self.actions_history.append(action)
                results.append(result)
            
            self.state = AgentState.COMPLETED
            logger.info(f"[{self.name}] Completed execution")
            
            return {
                "status": "success",
                "agent": self.name,
                "results": results,
                "thought": thought_result
            }
            
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"[{self.name}] Error: {str(e)}")
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }
    
    def add_to_memory(self, message: AgentMessage):
        """Add a message to agent's memory."""
        self.memory.append(message)
        
    def get_memory_context(self, limit: int = 10) -> List[Dict]:
        """Get recent memory for context."""
        return [
            {"role": m.role, "content": m.content}
            for m in self.memory[-limit:]
        ]
    
    def reset(self):
        """Reset agent state."""
        self.state = AgentState.IDLE
        self.memory.clear()
        self.actions_history.clear()
