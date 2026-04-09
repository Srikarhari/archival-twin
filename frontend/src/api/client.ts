import type {
  HealthResponse,
  ConfigResponse,
  MatchResponse,
  MatchError,
} from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "";

export async function getHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BASE}/api/health`);
  return res.json();
}

export async function getConfig(): Promise<ConfigResponse> {
  const res = await fetch(`${BASE}/api/config`);
  return res.json();
}

export async function postMatch(
  imageBase64: string,
): Promise<MatchResponse | MatchError> {
  const res = await fetch(`${BASE}/api/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imageBase64 }),
  });
  return res.json();
}
