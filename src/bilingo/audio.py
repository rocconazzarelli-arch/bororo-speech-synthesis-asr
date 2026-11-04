"""Audio and filename utilities shared by the BiLingo pipelines."""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata

import numpy as np


def sanitize_filename(text: str, max_length: int = 80) -> str:
    """Return a readable, deterministic and collision-resistant file stem."""
    normalized = unicodedata.normalize("NFKD", text.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9_-]+", "_", ascii_text).strip("_") or "term"
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    prefix_length = max(1, max_length - len(digest) - 1)
    return f"{slug[:prefix_length]}-{digest}"


def add_white_noise(
    waveform: np.ndarray,
    snr_db: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Add white noise at a target signal-to-noise ratio in decibels."""
    waveform = np.asarray(waveform, dtype=np.float32)
    if waveform.size == 0:
        return waveform.copy()

    signal_power = float(np.mean(waveform**2))
    if signal_power <= 1e-12:
        return waveform.copy()

    noise_power = signal_power / (10 ** (snr_db / 10.0))
    noise = rng.normal(0.0, 1.0, size=waveform.shape).astype(np.float32)
    noise_scale = math.sqrt(noise_power / (float(np.mean(noise**2)) + 1e-12))
    return np.clip(waveform + noise * noise_scale, -1.0, 1.0).astype(np.float32)
