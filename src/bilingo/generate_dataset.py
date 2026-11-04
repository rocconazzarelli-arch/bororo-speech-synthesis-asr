"""Generate a synthetic Bororo speech dataset with Meta MMS-TTS."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, VitsModel

from .audio import add_white_noise, sanitize_filename


DEFAULT_MODEL = "facebook/mms-tts-bor"


def load_dictionary(path: Path) -> dict[str, str]:
    """Load simple and BiLGraph-style dictionary exports."""
    with path.open(encoding="utf-8") as stream:
        raw: Any = json.load(stream)
    if not isinstance(raw, dict):
        raise ValueError("The dictionary must be a JSON object.")

    terms: dict[str, str] = {}
    for key, value in raw.items():
        term = str(key).strip()
        if not term:
            continue
        if isinstance(value, dict):
            gloss = str(value.get("desc", ""))
        else:
            gloss = str(value)
        terms[term] = gloss
    return terms


@torch.inference_mode()
def synthesize(model: VitsModel, tokenizer: AutoTokenizer, text: str, device: str) -> np.ndarray:
    inputs = tokenizer(text, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    waveform = model(**inputs).waveform[0]
    return waveform.detach().cpu().numpy().astype(np.float32)


def generate_dataset(
    dictionary_path: Path,
    output_dir: Path,
    samples_per_term: int = 50,
    snr_db: float = 20.0,
    seed: int = 1234,
    limit: int | None = None,
    model_id: str = DEFAULT_MODEL,
) -> Path:
    if samples_per_term < 1:
        raise ValueError("samples_per_term must be at least 1")
    if not dictionary_path.exists():
        raise FileNotFoundError(dictionary_path)

    dictionary = load_dictionary(dictionary_path)
    selected_terms = sorted(dictionary)
    if limit is not None:
        selected_terms = selected_terms[:limit]
    if not selected_terms:
        raise ValueError("The dictionary contains no usable terms.")

    output_dir.mkdir(parents=True, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id).to(device).eval()
    sample_rate = int(model.config.sampling_rate)
    rng = np.random.default_rng(seed)

    manifest_path = output_dir / "manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["audio", "transcript", "gloss_pt", "snr_db", "sample_rate"],
        )
        writer.writeheader()
        for term in tqdm(selected_terms, desc="Bororo terms"):
            term_dir = output_dir / sanitize_filename(term)
            term_dir.mkdir(parents=True, exist_ok=True)
            clean_waveform = synthesize(model, tokenizer, term, device)
            for index in range(samples_per_term):
                noisy_waveform = add_white_noise(clean_waveform, snr_db, rng)
                audio_path = term_dir / f"sample_{index:03d}.wav"
                sf.write(audio_path, noisy_waveform, sample_rate)
                writer.writerow(
                    {
                        "audio": audio_path.relative_to(output_dir).as_posix(),
                        "transcript": term,
                        "gloss_pt": dictionary[term],
                        "snr_db": snr_db,
                        "sample_rate": sample_rate,
                    }
                )
    return manifest_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dictionary", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/mms_bororo_audio"))
    parser.add_argument("--samples-per-term", type=int, default=50)
    parser.add_argument("--snr-db", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    manifest = generate_dataset(
        dictionary_path=args.dictionary,
        output_dir=args.output,
        samples_per_term=args.samples_per_term,
        snr_db=args.snr_db,
        seed=args.seed,
        limit=args.limit,
        model_id=args.model,
    )
    print(f"Manifest written to {manifest}")


if __name__ == "__main__":
    main()
