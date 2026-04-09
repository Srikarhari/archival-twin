"""Pydantic request/response models for all API routes."""

from pydantic import BaseModel


class MatchRequest(BaseModel):
    image: str  # base64-encoded JPEG
    capture_timestamp: str | None = None


class StageResult(BaseModel):
    completed: bool
    duration_ms: float


class TwinMetadata(BaseModel):
    source_collection: str | None = None
    title: str | None = None
    creator_photographer: str | None = None
    date_text: str | None = None
    place_text: str | None = None
    source_url: str | None = None
    rights_text: str | None = None


class TwinResult(BaseModel):
    match_id: int
    source_item_id: str | None = None
    filename: str
    image_url: str
    latest_match_url: str
    similarity_score: float
    confidence_label: str
    pose_tag: str
    age_band: str
    dominant_emotion: str
    original_caption: str | None = None
    generated_caption: str
    metadata: TwinMetadata


class MatchResponse(BaseModel):
    matched: bool
    twin: TwinResult
    disclosure_text: str
    stages: dict[str, StageResult]
    total_duration_ms: float


class MatchError(BaseModel):
    matched: bool = False
    error: str
    detail: str
    face_count: int | None = None


class HealthResponse(BaseModel):
    status: str
    face_engine: str
    archive_count: int
    gpu_available: bool
    version: str = "0.1.0"


class ConfigResponse(BaseModel):
    version: str = "0.1.0"
    collections: list[str]
    auto_capture_enabled: bool = False
    capture_cooldown_ms: int = 3000
