# Speaker Similarity

Bhasha can evaluate voice-cloning similarity by comparing speaker embeddings from a reference clip and a generated clip.

```text
reference voice audio -> speaker embedding
generated audio -> speaker embedding
cosine(reference, generated) -> speaker_similarity
```

## What It Measures

Speaker similarity estimates whether generated speech sounds like the reference speaker according to an embedding model. It should be paired with human A/B listening for serious cloning evaluation.

## Command

```bash
python -m bhasha eval-speaker --run-dir outputs/runs/<run_id> --device cpu
```

## Outputs

- Updates `benchmark.csv`: `speaker_embedding_model`, `speaker_similarity`.
- Writes `speaker_similarity.json` with reference/generated clip paths and scores.

## Applicability

- Voice-cloning models: score is computed when reference audio exists.
- Non-cloning models: `not_applicable`.
- Missing reference clip: `missing_reference_audio`.

Thresholds depend on the embedding model, so reports must name the embedding model used.
