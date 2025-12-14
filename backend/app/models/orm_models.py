# backend/app/models/orm_models.py

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship

from app.models.db import Base


# --------------------------------------------------
# Source Table
# --------------------------------------------------
class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False, default="rss")  # rss / api / html / youtube
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one source → many news items
    news_items = relationship("NewsItem", back_populates="source")


# --------------------------------------------------
# News Item Table
# --------------------------------------------------
class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    url = Column(String(1000), unique=True)
    published_at = Column(DateTime)
    retrieved_at = Column(DateTime, default=datetime.utcnow)

    # Embedding stored as JSON (for pgvector you will change this)
    embedding = Column(JSON, nullable=True)

    # Tags, keywords, entities (NER)
    tags = Column(JSON, nullable=True)

    # Duplicate handling
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, ForeignKey("news_items.id"), nullable=True)  # points to original
    cluster_id = Column(Integer, nullable=True)  # used for clustering (optional)

    # Full article text (optional)
    content = Column(Text, nullable=True)

    # Relationships
    source = relationship("Source", back_populates="news_items")
    favorites = relationship("Favorite", back_populates="news_item")


# --------------------------------------------------
# Favorites Table
# --------------------------------------------------
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # optional for MVP
    news_item_id = Column(Integer, ForeignKey("news_items.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    news_item = relationship("NewsItem", back_populates="favorites")
    user = relationship("User", back_populates="favorites")


# --------------------------------------------------
# Broadcast Logs Table
# --------------------------------------------------
class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"

    id = Column(Integer, primary_key=True, index=True)

    favorite_id = Column(Integer, ForeignKey("favorites.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # email / linkedin / whatsapp / blog / newsletter
    status = Column(String(100), nullable=False, default="success")

    message_preview = Column(Text, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    favorite = relationship("Favorite")


# --------------------------------------------------
# User Table (optional for multi-user; simple for MVP)
# --------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    role = Column(String(50), default="user")  # admin/user

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    favorites = relationship("Favorite", back_populates="user")
