"""Topics, interaction history, interests, recommendations, and knowledge links."""
from datetime import datetime
from sqlalchemy import (
    CheckConstraint, ForeignKey, Index, Numeric, String, Text, UniqueConstraint,
    DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, ID_TYPE


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ResourceTopic(Base):
    __tablename__ = "resource_topics"
    __table_args__ = (CheckConstraint("relevance_weight >= 0 AND relevance_weight <= 1", name="ck_resource_topic_weight"),)
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("topics.id"), primary_key=True)
    relevance_weight: Mapped[float] = mapped_column(Numeric(8, 5), nullable=False)


class UserInteraction(Base):
    __tablename__ = "user_interactions"
    __table_args__ = (
        CheckConstraint("interaction_type IN ('search', 'view', 'download', 'borrow', 'reserve', 'return', 'rating')", name="ck_interaction_type"),
        CheckConstraint(
            "(interaction_type = 'search' AND search_query IS NOT NULL) OR "
            "(interaction_type <> 'search' AND (search_query IS NULL OR length(search_query) >= 0))",
            name="ck_interaction_payload",
        ),
        Index("ix_user_interactions_resource_id", "resource_id"),
        Index("ix_user_interactions_user_id", "user_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), nullable=False)
    resource_id: Mapped[int | None] = mapped_column(ID_TYPE, ForeignKey("resources.id"))
    interaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    search_query: Mapped[str | None] = mapped_column(String(500))
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())


class UserInterest(Base):
    __tablename__ = "user_interests"
    __table_args__ = (CheckConstraint("interest_weight >= 0 AND interest_weight <= 1", name="ck_user_interest_weight"),)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("topics.id"), primary_key=True)
    interest_weight: Mapped[float] = mapped_column(Numeric(8, 5), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        CheckConstraint("relevance_score >= 0 AND relevance_score <= 1", name="ck_recommendation_score"),
        Index("ix_recommendations_resource_id", "resource_id"),
        Index("ix_recommendations_user_id", "user_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("users.id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), nullable=False)
    relevance_score: Mapped[float] = mapped_column(Numeric(8, 5), nullable=False)
    recommendation_reason: Mapped[str | None] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    model_version: Mapped[str | None] = mapped_column(String(50))


class KnowledgeLink(Base):
    __tablename__ = "knowledge_links"
    __table_args__ = (
        UniqueConstraint("source_resource_id", "target_resource_id", "relationship_type", name="uq_knowledge_link"),
        CheckConstraint("source_resource_id <> target_resource_id", name="ck_knowledge_distinct"),
        CheckConstraint("strength >= 0 AND strength <= 1", name="ck_knowledge_strength"),
        Index("ix_knowledge_links_source_resource_id", "source_resource_id"),
        Index("ix_knowledge_links_target_resource_id", "target_resource_id"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, primary_key=True, autoincrement=True)
    source_resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), nullable=False)
    target_resource_id: Mapped[int] = mapped_column(ID_TYPE, ForeignKey("resources.id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False)
    strength: Mapped[float] = mapped_column(Numeric(8, 5), nullable=False)
