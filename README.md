# Bororo Speech Synthesis and ASR Benchmark

An experimental speech pipeline for **Bororo**, a low-resource Indigenous language spoken in Brazil. The project generates synthetic speech with Meta's MMS-TTS model, creates controlled noisy variants, and benchmarks automatic speech recognition with Whisper using WER and CER.

## Why this project

Modern speech systems have limited coverage for low-resource languages. This project explores a reproducible way to create controlled audio samples and measure how an ASR model behaves when linguistic resources are scarce.

## Pipeline

1. Load an authorized Bororo–Portuguese dictionary export.
2. Generate speech with `facebook/mms-tts-bor`.
3. Add white noise at a configurable signal-to-noise ratio.
4. Save WAV files and a manifest containing reference transcripts.
5. Transcribe the samples with Whisper.
6. Compute Word Error Rate (WER) and Character Error Rate (CER).

## Repository structure

```text
.
├── notebooks/
│   ├── 01_generate_synthetic_speech.ipynb
│   └── 02_benchmark_whisper.ipynb
├── data/
│   └── README.md
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place an authorized dictionary file at `data/boe-dict-20240805.json`. For the API-based benchmark, expose the credential through the environment:

```bash
export OPENAI_API_KEY="..."
```

Never commit API keys, generated audio archives, or local virtual environments.

## Current status

The repository contains the generation and evaluation workflow. Aggregate WER/CER results are intentionally not claimed because the full benchmark output was not present in the original project files and the source dictionary's redistribution terms were not documented.

## Responsible use

Synthetic speech is not a substitute for community-governed, consent-based language data. Any extension of this work should involve Indigenous language stakeholders and respect data sovereignty, attribution, and licensing requirements.

## Author

Rocco Nazzarelli

M.Sc. Computer Science and Engineering – Artificial Intelligence, Politecnico di Milano
