"""
Configuration Settings Module
Handles all application configuration using Pydantic.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path


class HuggingFaceSettings(BaseSettings):
    """HuggingFace API Configuration."""
    
    api_key: str = Field(default="", alias="HUGGINGFACE_API_KEY")
    default_llm_model: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.2",
        alias="DEFAULT_LLM_MODEL"
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL"
    )
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class GitHubSettings(BaseSettings):
    """GitHub API Configuration."""
    
    access_token: Optional[str] = Field(default=None, alias="GITHUB_ACCESS_TOKEN")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class DatabaseSettings(BaseSettings):
    """Database Configuration."""
    
    url: str = Field(
        default="sqlite:///./career_architect.db",
        alias="DATABASE_URL"
    )
    
    class Config:
        env_file = ".env"
        extra = "ignore"


class AppSettings(BaseSettings):
    """Main Application Settings."""
    
    env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Sub-settings
    huggingface: HuggingFaceSettings = Field(default_factory=HuggingFaceSettings)
    github: GitHubSettings = Field(default_factory=GitHubSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"
    templates_dir: Path = base_dir / "templates"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


# Global settings instance
settings = AppSettings()


def get_settings() -> AppSettings:
    """Get application settings singleton."""
    return settings


# Model configurations for different tasks
MODEL_CONFIGS = {
    "text_generation": {
        "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
        "task": "text-generation",
        "max_new_tokens": 512,
        "temperature": 0.7,
    },
    "summarization": {
        "model_id": "facebook/bart-large-cnn",
        "task": "summarization",
        "max_length": 150,
    },
    "embedding": {
        "model_id": "sentence-transformers/all-MiniLM-L6-v2",
        "task": "feature-extraction",
    },
    "classification": {
        "model_id": "facebook/bart-large-mnli",
        "task": "zero-shot-classification",
    },
    "ner": {
        "model_id": "dslim/bert-base-NER",
        "task": "token-classification",
    },
}


# Industry and role configurations
SUPPORTED_INDUSTRIES = [
    "Technology", "Finance", "Healthcare", "Marketing",
    "Consulting", "Education", "Manufacturing", "Retail",
    "Media", "Non-profit"
]

SUPPORTED_ROLES = [
    "Software Engineer", "Data Scientist", "Product Manager",
    "UX Designer", "Business Analyst", "Marketing Manager",
    "Sales Representative", "HR Manager", "Operations Manager",
    "Financial Analyst"
]

# Portfolio layout configurations
PORTFOLIO_LAYOUTS = {
    "developer": ["hero", "skills", "projects", "experience", "contact"],
    "analyst": ["hero", "metrics", "skills", "experience", "projects", "contact"],
    "designer": ["hero", "portfolio", "skills", "experience", "contact"],
    "manager": ["hero", "experience", "achievements", "skills", "contact"],
    "default": ["hero", "about", "skills", "experience", "projects", "contact"]
}
