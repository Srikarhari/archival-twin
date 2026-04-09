export interface StageResult {
  completed: boolean;
  duration_ms: number;
}

export interface TwinMetadata {
  source_collection: string | null;
  title: string | null;
  creator_photographer: string | null;
  date_text: string | null;
  place_text: string | null;
  source_url: string | null;
  rights_text: string | null;
}

export interface TwinResult {
  match_id: number;
  source_item_id: string | null;
  filename: string;
  image_url: string;
  latest_match_url: string;
  similarity_score: number;
  confidence_label: string;
  pose_tag: string;
  age_band: string;
  original_caption: string | null;
  generated_caption: string;
  metadata: TwinMetadata;
}

export interface MatchResponse {
  matched: boolean;
  twin: TwinResult;
  disclosure_text: string;
  stages: Record<string, StageResult>;
  total_duration_ms: number;
}

export interface MatchError {
  matched: false;
  error: string;
  detail: string;
  face_count?: number;
}

export interface HealthResponse {
  status: string;
  face_engine: string;
  archive_count: number;
  gpu_available: boolean;
  version: string;
}

export interface ConfigResponse {
  version: string;
  collections: string[];
  auto_capture_enabled: boolean;
  capture_cooldown_ms: number;
}
