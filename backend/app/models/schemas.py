# backend/app/models/schemas.py

from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, Field



# ============================================================
# Source Schemas
# ============================================================

class SourceBase(BaseModel):
    name: str
    url: str
    type: str = "rss"
    active: bool = True


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================
# News Item Schemas
# ============================================================

class NewsItemBase(BaseModel):
    title: str
    summary: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    tags: Optional[Any] = None  # list or dict
    is_duplicate: bool = False
    duplicate_of: Optional[int] = None
    cluster_id: Optional[int] = None
    content: Optional[str] = None


class NewsItemCreate(NewsItemBase):
    source_id: int
    embedding: Optional[Any] = None


class NewsItemResponse(NewsItemBase):
    id: int
    source_id: int
    retrieved_at: datetime

    class Config:
        orm_mode = True


# ============================================================
# Favorite Schemas
# ============================================================

class FavoriteBase(BaseModel):
    news_item_id: int


class FavoriteCreate(FavoriteBase):
    user_id: Optional[int] = None  # optional for MVP


class FavoriteResponse(BaseModel):
    id: int
    user_id: Optional[int]
    news_item: NewsItemResponse
    created_at: datetime

    class Config:
        orm_mode = True


class BroadcastRequest(BaseModel):
    favorite_id: int
    platform: str


class BroadcastResponse(BaseModel):
    id: int
    status: str
    message_preview: str
    timestamp: datetime
# ============================================================
# User Schemas
# ============================================================

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = "user"


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================
# Generic Response Schemas
# ============================================================

class NewsListResponse(BaseModel):
    total: int
    items: List[NewsItemResponse]


class FavoriteListResponse(BaseModel):
    total: int
    items: List[FavoriteResponse]


class BroadcastRequest(BaseModel):
    favorite_id: int
    platform: str


class BroadcastResponse(BaseModel):
    id: int
    status: str
    message_preview: str
    timestamp: datetime

# ============================================================
# Pagination Schema (REQUIRED for /api/v1/news)
# ============================================================

class PaginatedNewsResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[NewsItemResponse]