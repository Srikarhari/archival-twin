# Archival Twin

An art-installation web app that finds a visitor's closest visual match in a colonial-era photographic archive.

A visitor stands before a camera. The system captures their face, compares it against a pre-built archive of historical photographs, and returns the single closest match — exposing the mechanics of machine vision and the assumptions embedded in archival classification systems.

## Project Structure

- `backend/` — Python FastAPI server (face detection, embedding, matching)
- `frontend/` — React + Vite client (webcam capture, split-screen display)
- `Faces_FullArchive/` — Pre-built archive of face images (not tracked in git)
- `Latest_match/` — Output folder for the most recent match (single file, overwritten)
- `docs/` — Setup, deployment, and ethics documentation

## Quick Start

See `docs/installation_setup.md` for full instructions.

## Target Collections

- NYPL People of India
- British Museum / Maurice Vidal Portman (Andaman Islands)

## Ethics

This system does not classify visitors by race, ethnicity, caste, nationality, religion, or any protected trait. See `docs/ethics_notes.md`.
