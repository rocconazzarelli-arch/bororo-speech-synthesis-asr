# Source inventory

The original local project folder was consolidated rather than copied verbatim.

| Local material | Repository treatment |
| --- | --- |
| `AUDIO_GENERATION_DEFINITE.ipynb` | Preserved as notebook 01 and refactored into `bilingo.generate_dataset`. |
| `BENCHMARK_WHISPER.ipynb` | Preserved as notebook 02 with portable paths and environment-based credentials. |
| `Speech-Annotator.ipynb` | Experimental audio conversion and MMS transcription logic was distilled into `bilingo.transcribe`; the raw notebook was not published because it contains local cloud configuration, duplicated cells and an interrupted execution. |
| `MMS_Script.py` and `MMS_Script_Rocco.py` | Duplicated prototype scripts were replaced by the tested package modules. |
| `Copy of mms-tts-bor.ipynb` | Excluded because it duplicates the model-loading example already covered by notebook 01. |
| `ROCCO PROJECT.docx` | Consolidated into `PROJECT_PLAN.md`. |
| Bororo dictionary JSON exports | Excluded pending clear redistribution terms; documented under `data/README.md`. |
| Research PDF copies | Cited in `REFERENCES.md` rather than redistributed. |
| `.venv`, `bororo_env`, `new_env` | Excluded as machine-specific environments. |

This structure keeps the public repository focused, reproducible and free of local credentials or third-party document copies.
