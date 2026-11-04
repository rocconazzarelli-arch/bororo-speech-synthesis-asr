# Architecture

BiLingo separates data ownership, model execution and evaluation so that sensitive or community-governed language resources do not need to be stored in the public code repository.

```text
Authorized dictionary
        |
        v
MMS-TTS generation --> controlled augmentation --> WAV files + manifest
                                                      |
                             +------------------------+------------------+
                             |                                           |
                             v                                           v
                    local MMS ASR                              Whisper benchmark
                             |                                           |
                             +------------------------+------------------+
                                                      v
                                             WER / CER / coverage
```

## Components

- `bilingo.audio`: deterministic filenames and signal-level augmentation.
- `bilingo.generate_dataset`: CLI and reusable generator for synthetic audio datasets.
- `bilingo.transcribe`: experimental local transcription baseline for browser/mobile recordings.
- `notebooks/01_generate_synthetic_speech.ipynb`: inspectable generation walkthrough.
- `notebooks/02_benchmark_whisper.ipynb`: API-based evaluation workflow.

## Data boundary

Dictionary exports, community recordings, generated audio, cloud credentials and benchmark artifacts remain outside version control. This is both a licensing safeguard and a privacy/security boundary.
