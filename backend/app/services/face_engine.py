"""InsightFace wrapper — primary face detection and embedding engine."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

from app.config import settings

logger = logging.getLogger(__name__)


class NoFaceDetected(Exception):
    pass


class MultipleFacesDetected(Exception):
    def __init__(self, count: int) -> None:
        self.count = count
        super().__init__(f"Detected {count} faces, expected exactly 1")


@dataclass
class FaceResult:
    embedding: np.ndarray       # 512-d float32, L2-normalized
    bbox: tuple[float, float, float, float]  # x, y, w, h
    detection_score: float
    pose_tag: str               # "frontal", "three_quarter", "profile"
    age_band: str               # age range or "unknown"


class FaceEngine:
    """Wraps InsightFace FaceAnalysis for detection + embedding."""

    def __init__(self) -> None:
        self._app = None
        self._available = False

    def initialize(self) -> None:
        try:
            from insightface.app import FaceAnalysis  # type: ignore[import-untyped]
        except ImportError:
            logger.error(
                "InsightFace is not installed. The face engine will be unavailable. "
                "Install with: pip install insightface onnxruntime"
            )
            return

        providers = [
            "CUDAExecutionProvider",
            "CoreMLExecutionProvider",
            "CPUExecutionProvider",
        ]
        logger.info("Initializing InsightFace model=%s", settings.insightface_model)
        self._app = FaceAnalysis(
            name=settings.insightface_model,
            providers=providers,
        )
        self._app.prepare(ctx_id=0, det_size=settings.det_size_tuple)
        self._available = True
        logger.info("InsightFace initialized. Providers: %s", self._app.models)

    @property
    def is_available(self) -> bool:
        return self._available

    @property
    def gpu_available(self) -> bool:
        if not self._available:
            return False
        try:
            import onnxruntime  # type: ignore[import-untyped]
            return "CUDAExecutionProvider" in onnxruntime.get_available_providers()
        except ImportError:
            return False

    def detect_and_embed(self, image_rgb: np.ndarray) -> FaceResult:
        """Detect exactly one face and return its embedding.

        Args:
            image_rgb: RGB image as numpy array (H, W, 3).

        Returns:
            FaceResult with embedding, bbox, score, pose_tag, age_band.

        Raises:
            NoFaceDetected: No face found in the image.
            MultipleFacesDetected: More than one face found.
            RuntimeError: Engine not available.
        """
        if not self._available or self._app is None:
            raise RuntimeError("Face engine is not available")

        faces = self._app.get(image_rgb)

        if len(faces) == 0:
            raise NoFaceDetected("No face could be detected in the submitted image")

        if len(faces) > 1:
            raise MultipleFacesDetected(len(faces))

        face = faces[0]

        # Bounding box: InsightFace returns [x1, y1, x2, y2]
        x1, y1, x2, y2 = face.bbox
        bbox = (float(x1), float(y1), float(x2 - x1), float(y2 - y1))

        # Detection confidence
        det_score = float(face.det_score)
        if det_score < settings.min_detection_score:
            raise NoFaceDetected(
                f"Face detected but confidence too low ({det_score:.2f} < {settings.min_detection_score})"
            )

        # Embedding: 512-d, already L2-normalized by InsightFace
        embedding = face.normed_embedding.astype(np.float32)

        # Pose estimation from yaw angle
        pose_tag = self._estimate_pose(face)

        # Age band
        age_band = self._estimate_age_band(face)

        return FaceResult(
            embedding=embedding,
            bbox=bbox,
            detection_score=det_score,
            pose_tag=pose_tag,
            age_band=age_band,
        )

    def _estimate_pose(self, face: object) -> str:
        """Estimate pose tag from face landmarks or pose attribute."""
        try:
            pose = getattr(face, "pose", None)
            if pose is not None:
                yaw = abs(float(pose[1]))  # pose is [pitch, yaw, roll]
                if yaw < 15:
                    return "frontal"
                elif yaw < 45:
                    return "three_quarter"
                else:
                    return "profile"
        except (IndexError, TypeError, AttributeError):
            pass
        return "unknown"

    def _estimate_age_band(self, face: object) -> str:
        """Estimate age band if InsightFace provides age attribute."""
        try:
            age = getattr(face, "age", None)
            if age is not None:
                age = int(age)
                if age < 18:
                    return "under_18"
                elif age < 30:
                    return "18-29"
                elif age < 45:
                    return "30-44"
                elif age < 60:
                    return "45-59"
                else:
                    return "60+"
        except (TypeError, ValueError):
            pass
        return "unknown"
