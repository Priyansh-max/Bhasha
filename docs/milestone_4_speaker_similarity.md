# Milestone 4: Speaker Similarity

Bhasha now supports optional speaker similarity evaluation for voice-cloning models.

```text
reference voice audio -> speaker embedding
generated audio -> speaker embedding
cosine(reference, generated) -> speaker_similarity
```

## Implemented

- Optional `reference_audio` field on prompts.
- Optional `reference_audio` and `reference_audio_by_language` model parameters.
- `bhasha.speaker_metrics.cosine_similarity`.
- Optional SpeechBrain ECAPA speaker embedding backend.
- `bhasha eval-speaker` CLI command.
- `speaker_similarity.json` evidence output.
- `benchmark.csv` update with `speaker_embedding_model` and `speaker_similarity`.

## Command

Install optional dependencies:

```bash
.venv\Scripts\python -m pip install -r requirements/speaker.txt
```

Evaluate a completed run:

```bash
.venv\Scripts\python -m bhasha eval-speaker --run-dir outputs\runs\<run_id> --device cpu
```

## Important Notes

Speaker similarity applies to cloning-capable models only. For non-cloning models like Piper, Bhasha records `not_applicable`.

If a cloning-capable model has no reference audio, Bhasha records `missing_reference_audio` instead of inventing a score.

The target assignment threshold is cosine similarity >= 0.75, but that threshold depends on the embedding model. Reports must name the speaker embedding model used.
