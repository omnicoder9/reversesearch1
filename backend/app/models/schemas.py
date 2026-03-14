from enum import Enum
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class InputType(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"
    NAME = "name"
    PHOTO_URL = "photo_url"


class SearchInput(BaseModel):
    username: str | None = Field(default=None, min_length=2, max_length=60)
    platform: str | None = Field(default=None, min_length=2, max_length=40)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=7, max_length=25)
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    photo_url: HttpUrl | None = None
    consent_confirmed: bool = Field(
        default=False,
        description="Must be true to run searches involving personal identifiers.",
    )


class AccountMatch(BaseModel):
    platform: str
    url: str
    confidence: int = Field(ge=0, le=100)
    rationale: str


class MentionMatch(BaseModel):
    source: str
    title: str
    url: str
    snippet: str
    confidence: int = Field(ge=0, le=100)


class PhotoMatch(BaseModel):
    source: str
    url: str
    confidence: int = Field(ge=0, le=100)


class ConnectionEdge(BaseModel):
    source: str
    target: str
    relation: str


class AggregatedProfile(BaseModel):
    primary_identifier: str
    accounts: list[AccountMatch] = []
    mentions: list[MentionMatch] = []
    photo_matches: list[PhotoMatch] = []
    graph_edges: list[ConnectionEdge] = []
    risk_notes: list[str] = []


class SearchStatus(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class SearchStartResponse(BaseModel):
    task_id: str
    status: Literal["PENDING"]


class SearchResultEnvelope(BaseModel):
    task_id: str
    status: SearchStatus
    result: AggregatedProfile | None = None
    error: str | None = None
