# BiLingo - Bororo Speech AI Toolkit

BiLingo is an experimental speech toolkit developed during an MSc exchange at the **Universidade de São Paulo (USP)**. It explores how text-to-speech, speech recognition and controlled audio augmentation can support educational applications for **Bororo**, a low-resource Indigenous language spoken in Brazil.

The repository turns the original research notebooks into a small, reusable Python package while preserving the notebooks as transparent experiment records.

## What is included

- Synthetic Bororo speech generation with Meta's `facebook/mms-tts-bor` model.
- Controlled white-noise augmentation with a reproducible target SNR.
- CSV manifests containing audio paths, reference text and Portuguese glosses.
- An experimental local Bororo ASR wrapper based on Meta MMS.
- A Whisper benchmark notebook that computes WER, CER, latency and lexical coverage.
- Project planning, architecture and research references.

## Repository structure

```text
.
├── data/
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_PLAN.md
│   ├── REFERENCES.md
│   └── SOURCE_INVENTORY.md
├── notebooks/
│   ├── 01_generate_synthetic_speech.ipynb
│   └── 02_benchmark_whisper.ipynb
├── src/bilingo/
│   ├── __init__.py
│   ├── audio.py
│   ├── generate_dataset.py
│   └── transcribe.py
├── tests/
│   └── test_audio.py
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Installation

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/rocconazzarelli-arch/Bororo-speech-synthesis-asr.git
cd Bororo-speech-synthesis-asr
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

The local transcription command also requires `ffmpeg` to be available on the system path.

## Data setup

The source folder contained Bororo dictionary exports, but no explicit redistribution license was bundled with them. They are therefore not committed to this public repository.

Place an authorized dictionary export at:

```text
data/boe-dict-20240805.json
```

The generator accepts either a simple mapping:

```json
{"bororo_term": "Portuguese gloss"}
```

or the richer BiLGraph-style dictionary where each value contains a `desc` field.

## Generate a synthetic dataset

Run a small smoke test before launching a full generation job:

```bash
bilingo-generate \
  --dictionary data/boe-dict-20240805.json \
  --output artifacts/mms_bororo_audio \
  --samples-per-term 3 \
  --limit 10
```

For a larger experiment, remove `--limit` and choose the required number of noisy variants.

## Transcribe local audio

The local ASR command accepts WAV directly and converts WebM/MP4/M4A through `ffmpeg`:

```bash
bilingo-transcribe path/to/recording.webm
```

MMS language coverage and adapter availability can change. Treat this command as an experimental baseline and verify the selected model before reporting results.

## Whisper benchmark

The companion notebook `notebooks/02_benchmark_whisper.ipynb` evaluates generated audio through the OpenAI audio transcription API. Set the credential through the environment and start with a small sample because API calls can incur costs:

```bash
export OPENAI_API_KEY="..."
```

No aggregate WER/CER result is claimed in this repository because a complete benchmark output was not present in the original project folder.

## Tests

The lightweight audio utilities can be tested without downloading a model:

```bash
python -m unittest discover -s tests
```

## Responsible use

Synthetic speech is not a substitute for community-governed and consent-based language data. Extensions of this work should involve Indigenous language stakeholders and respect data sovereignty, attribution, privacy and licensing requirements.

## Author

Rocco Nazzarelli

MSc, Computer Science and Engineering - Artificial Intelligence

Politecnico di Milano / Universidade de São Paulo
