"""
Database Models
SQLAlchemy ORM models for the application.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """User model for authentication and tracking."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profiles = relationship("Profile", back_populates="user")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Profile(Base):
    """User profile data model."""
    
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String(50))  # linkedin, resume, manual
    raw_data = Column(JSON)
    processed_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profiles")
    career_dna = relationship("CareerDNA", back_populates="profile", uselist=False)
    optimizations = relationship("Optimization", back_populates="profile")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "source": self.source,
            "processed_data": self.processed_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class CareerDNA(Base):
    """Career DNA analysis results model."""
    
    __tablename__ = "career_dna"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    archetype = Column(String(100))
    strengths = Column(JSON)
    skills = Column(JSON)
    trajectory = Column(JSON)
    market_fit = Column(JSON)
    embedding = Column(JSON)  # Vector embedding for similarity
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="career_dna")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "archetype": self.archetype,
            "strengths": self.strengths,
            "skills": self.skills,
            "trajectory": self.trajectory,
            "market_fit": self.market_fit
        }


class Optimization(Base):
    """LinkedIn optimization results model."""
    
    __tablename__ = "optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    optimization_type = Column(String(50))  # headline, about, experience
    original_content = Column(Text)
    optimized_content = Column(Text)
    score = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="optimizations")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "type": self.optimization_type,
            "original": self.original_content,
            "optimized": self.optimized_content,
            "score": self.score
        }


class Portfolio(Base):
    """Generated portfolio model."""
    
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    layout = Column(String(50))
    color_scheme = Column(String(50))
    content = Column(JSON)
    files = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "layout": self.layout,
            "color_scheme": self.color_scheme,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Metrics(Base):
    """User engagement metrics model."""
    
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    metric_type = Column(String(50))
    value = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "type": self.metric_type,
            "value": self.value,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }
