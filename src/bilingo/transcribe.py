"""Experimental local Bororo transcription with Meta MMS."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import torch
import torchaudio
from transformers import AutoProcessor, Wav2Vec2ForCTC


DEFAULT_MODEL = "facebook/mms-1b-all"
TARGET_SAMPLE_RATE = 16_000


def convert_to_wav(source: Path, destination: Path) -> None:
    """Convert a browser/mobile recording to mono 16 kHz WAV with ffmpeg."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-ac",
            "1",
            "-ar",
            str(TARGET_SAMPLE_RATE),
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


class BororoTranscriber:
    def __init__(self, model_id: str = DEFAULT_MODEL, language: str = "bor") -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = AutoProcessor.from_pretrained(model_id, target_lang=language)
        self.model = Wav2Vec2ForCTC.from_pretrained(
            model_id,
            target_lang=language,
            ignore_mismatched_sizes=True,
        ).to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def transcribe_wav(self, path: Path) -> str:
        waveform, sample_rate = torchaudio.load(path)
        waveform = waveform.mean(dim=0)
        if sample_rate != TARGET_SAMPLE_RATE:
            waveform = torchaudio.functional.resample(
                waveform,
                sample_rate,
                TARGET_SAMPLE_RATE,
            )
        inputs = self.processor(
            waveform.numpy(),
            return_tensors="pt",
            sampling_rate=TARGET_SAMPLE_RATE,
        )
        logits = self.model(inputs.input_values.to(self.device)).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(predicted_ids)[0].strip()

    def transcribe(self, path: Path) -> str:
        if path.suffix.lower() == ".wav":
            return self.transcribe_wav(path)
        with tempfile.TemporaryDirectory(prefix="bilingo_") as temporary_dir:
            converted = Path(temporary_dir) / "audio.wav"
            convert_to_wav(path, converted)
            return self.transcribe_wav(converted)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default="bor")
    args = parser.parse_args()
    if not args.audio.exists():
        raise FileNotFoundError(args.audio)
    print(BororoTranscriber(args.model, args.language).transcribe(args.audio))


if __name__ == "__main__":
    main()
