# Project plan

This document distills the original BiLingo project notes into an implementation-oriented roadmap.

## Phase 1 - Dataset generation

- Load an authorized Boe/Bororo dictionary export.
- Generate one clean MMS-TTS waveform for every selected word.
- Produce reproducible noisy variants at configurable SNR levels.
- Extend generation from isolated terms to sentences from the Bororo treebank.
- Record synthesis coverage, failures and model/runtime metadata.

## Phase 2 - Speech processing evaluation

- Establish ASR baselines for Whisper and local MMS models.
- Evaluate generated Bororo audio with WER, CER, latency and lexical coverage.
- Compare clean and noisy audio conditions.
- Add configurable scoring for speaking exercises.
- Investigate model compression only after baseline quality is measured.

## Phase 3 - Application integration

- Accept WebM/mobile recordings from the BiLingo client.
- Convert audio to a consistent mono 16 kHz representation.
- Keep storage credentials outside source control.
- Return transcripts and evaluation feedback through a service boundary.
- Validate the workflow with language stakeholders before using real community data.

## Current repository status

- Synthetic word generation: implemented.
- Controlled noise augmentation: implemented.
- Dataset manifest: implemented.
- Whisper benchmark workflow: implemented, full experiment not yet recorded.
- Local MMS transcription baseline: experimental.
- Sentence-level generation and application API: planned.
