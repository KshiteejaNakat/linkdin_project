"""
Repository Pattern Implementation
Data access layer for database operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from loguru import logger

from .models import User, Profile, CareerDNA, Optimization, Portfolio, Metrics


class BaseRepository:
    """Base repository with common CRUD operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def commit(self):
        """Commit current transaction."""
        self.session.commit()
    
    def rollback(self):
        """Rollback current transaction."""
        self.session.rollback()


class UserRepository(BaseRepository):
    """Repository for User operations."""
    
    def create(self, email: str, name: str) -> User:
        """Create a new user."""
        user = User(email=email, name=name)
        self.session.add(user)
        self.session.flush()
        logger.info(f"Created user: {email}")
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.session.query(User).filter(User.email == email).first()
    
    def get_or_create(self, email: str, name: str) -> User:
        """Get existing user or create new one."""
        user = self.get_by_email(email)
        if user:
            return user
        return self.create(email, name)
    
    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user attributes."""
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.flush()
        return user


class ProfileRepository(BaseRepository):
    """Repository for Profile operations."""
    
    def create(
        self,
        user_id: int,
        source: str,
        raw_data: Dict[str, Any],
        processed_data: Optional[Dict[str, Any]] = None
    ) -> Profile:
        """Create a new profile."""
        profile = Profile(
            user_id=user_id,
            source=source,
            raw_data=raw_data,
            processed_data=processed_data or {}
        )
        self.session.add(profile)
        self.session.flush()
        return profile
    
    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Get profile by ID."""
        return self.session.query(Profile).filter(Profile.id == profile_id).first()
    
    def get_by_user(self, user_id: int) -> List[Profile]:
        """Get all profiles for a user."""
        return self.session.query(Profile).filter(Profile.user_id == user_id).all()
    
    def get_latest_by_user(self, user_id: int) -> Optional[Profile]:
        """Get most recent profile for a user."""
        return (
            self.session.query(Profile)
            .filter(Profile.user_id == user_id)
            .order_by(Profile.created_at.desc())
            .first()
        )
    
    def update_processed_data(
        self,
        profile_id: int,
        processed_data: Dict[str, Any]
    ) -> Optional[Profile]:
        """Update processed data for a profile."""
        profile = self.get_by_id(profile_id)
        if profile:
            profile.processed_data = processed_data
            self.session.flush()
        return profile


class CareerDNARepository(BaseRepository):
    """Repository for Career DNA operations."""
    
    def create(self, profile_id: int, dna_data: Dict[str, Any]) -> CareerDNA:
        """Create Career DNA entry."""
        career_dna = CareerDNA(
            profile_id=profile_id,
            archetype=dna_data.get("archetype"),
            strengths=dna_data.get("strengths"),
            skills=dna_data.get("skills"),
            trajectory=dna_data.get("trajectory"),
            market_fit=dna_data.get("market_fit"),
            embedding=dna_data.get("embedding")
        )
        self.session.add(career_dna)
        self.session.flush()
        return career_dna
    
    def get_by_profile(self, profile_id: int) -> Optional[CareerDNA]:
        """Get Career DNA for a profile."""
        return (
            self.session.query(CareerDNA)
            .filter(CareerDNA.profile_id == profile_id)
            .first()
        )


class OptimizationRepository(BaseRepository):
    """Repository for Optimization operations."""
    
    def create(
        self,
        profile_id: int,
        optimization_type: str,
        original: str,
        optimized: str,
        score: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optimization:
        """Create optimization entry."""
        opt = Optimization(
            profile_id=profile_id,
            optimization_type=optimization_type,
            original_content=original,
            optimized_content=optimized,
            score=score,
            metadata=metadata or {}
        )
        self.session.add(opt)
        self.session.flush()
        return opt
    
    def get_by_profile(self, profile_id: int) -> List[Optimization]:
        """Get all optimizations for a profile."""
        return (
            self.session.query(Optimization)
            .filter(Optimization.profile_id == profile_id)
            .all()
        )
