"""
Model Selector Module
Selects optimal models for different tasks.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class TaskType(Enum):
    """Supported task types."""
    TEXT_GENERATION = "text-generation"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "zero-shot-classification"
    EMBEDDING = "feature-extraction"
    NER = "token-classification"
    QUESTION_ANSWERING = "question-answering"


@dataclass
class ModelConfig:
    """Configuration for a model."""
    model_id: str
    task: TaskType
    description: str
    max_input_length: int
    recommended_for: List[str]
    performance_tier: str  # fast, balanced, quality


class ModelSelector:
    """
    Selects optimal models for different tasks based on
    requirements and constraints.
    """
    
    def __init__(self):
        self.models = self._load_model_configs()
        
    def _load_model_configs(self) -> Dict[str, ModelConfig]:
        """Load available model configurations."""
        return {
            # Text Generation Models
            "mistral-7b": ModelConfig(
                model_id="mistralai/Mistral-7B-Instruct-v0.2",
                task=TaskType.TEXT_GENERATION,
                description="High-quality instruction-tuned model",
                max_input_length=8192,
                recommended_for=["content_generation", "creative_writing"],
                performance_tier="quality"
            ),
            "phi-2": ModelConfig(
                model_id="microsoft/phi-2",
                task=TaskType.TEXT_GENERATION,
                description="Fast and efficient small model",
                max_input_length=2048,
                recommended_for=["quick_responses", "simple_tasks"],
                performance_tier="fast"
            ),
            "zephyr-7b": ModelConfig(
                model_id="HuggingFaceH4/zephyr-7b-beta",
                task=TaskType.TEXT_GENERATION,
                description="Balanced performance model",
                max_input_length=4096,
                recommended_for=["general_purpose", "chat"],
                performance_tier="balanced"
            ),
            
            # Summarization Models
            "bart-large-cnn": ModelConfig(
                model_id="facebook/bart-large-cnn",
                task=TaskType.SUMMARIZATION,
                description="News-style summarization",
                max_input_length=1024,
                recommended_for=["article_summary", "content_condensing"],
                performance_tier="quality"
            ),
            "t5-base": ModelConfig(
                model_id="t5-base",
                task=TaskType.SUMMARIZATION,
                description="Versatile text-to-text model",
                max_input_length=512,
                recommended_for=["general_summarization"],
                performance_tier="balanced"
            ),
            
            # Embedding Models
            "minilm": ModelConfig(
                model_id="sentence-transformers/all-MiniLM-L6-v2",
                task=TaskType.EMBEDDING,
                description="Fast semantic embeddings",
                max_input_length=256,
                recommended_for=["similarity_search", "clustering"],
                performance_tier="fast"
            ),
            "mpnet": ModelConfig(
                model_id="sentence-transformers/all-mpnet-base-v2",
                task=TaskType.EMBEDDING,
                description="High-quality embeddings",
                max_input_length=384,
                recommended_for=["semantic_search", "retrieval"],
                performance_tier="quality"
            ),
            
            # Classification Models
            "bart-mnli": ModelConfig(
                model_id="facebook/bart-large-mnli",
                task=TaskType.CLASSIFICATION,
                description="Zero-shot classification",
                max_input_length=1024,
                recommended_for=["categorization", "intent_detection"],
                performance_tier="quality"
            ),
            
            # NER Models
            "bert-ner": ModelConfig(
                model_id="dslim/bert-base-NER",
                task=TaskType.NER,
                description="Named entity recognition",
                max_input_length=512,
                recommended_for=["entity_extraction", "resume_parsing"],
                performance_tier="balanced"
            )
        }
    
    def select_model(
        self,
        task: TaskType,
        use_case: Optional[str] = None,
        performance_priority: str = "balanced"
    ) -> ModelConfig:
        """Select optimal model for task."""
        # Filter by task
        candidates = [
            m for m in self.models.values()
            if m.task == task
        ]
        
        if not candidates:
            logger.warning(f"No models found for task: {task}")
            return list(self.models.values())[0]
        
        # Filter by use case if provided
        if use_case:
            use_case_matches = [
                m for m in candidates
                if use_case in m.recommended_for
            ]
            if use_case_matches:
                candidates = use_case_matches
        
        # Filter by performance tier
        tier_matches = [
            m for m in candidates
            if m.performance_tier == performance_priority
        ]
        if tier_matches:
            candidates = tier_matches
        
        return candidates[0]
    
    def get_model_for_headline(self) -> ModelConfig:
        """Get model optimized for headline generation."""
        return self.select_model(
            TaskType.TEXT_GENERATION,
            use_case="content_generation",
            performance_priority="quality"
        )
    
    def get_model_for_about(self) -> ModelConfig:
        """Get model for About section generation."""
        return self.select_model(
            TaskType.TEXT_GENERATION,
            use_case="creative_writing",
            performance_priority="quality"
        )
    
    def get_model_for_embedding(self) -> ModelConfig:
        """Get model for text embeddings."""
        return self.select_model(
            TaskType.EMBEDDING,
            use_case="semantic_search",
            performance_priority="balanced"
        )
    
    def get_model_for_classification(self) -> ModelConfig:
        """Get model for text classification."""
        return self.select_model(
            TaskType.CLASSIFICATION,
            use_case="categorization",
            performance_priority="quality"
        )
    
    def get_model_for_resume_parsing(self) -> ModelConfig:
        """Get model for resume parsing/NER."""
        return self.select_model(
            TaskType.NER,
            use_case="entity_extraction",
            performance_priority="balanced"
        )
    
    def list_available_models(self, task: Optional[TaskType] = None) -> List[Dict]:
        """List available models."""
        models = self.models.values()
        
        if task:
            models = [m for m in models if m.task == task]
        
        return [
            {
                "id": m.model_id,
                "task": m.task.value,
                "description": m.description,
                "tier": m.performance_tier
            }
            for m in models
        ]
    
    def get_model_info(self, model_key: str) -> Optional[ModelConfig]:
        """Get information about a specific model."""
        return self.models.get(model_key)
