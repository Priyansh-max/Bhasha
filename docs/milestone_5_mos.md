# Milestone 5: MOS Aggregation

Bhasha now supports MOS aggregation from real listener ratings.

```text
generated audio -> human listener ratings -> average MOS per sample
```

## Implemented

- `bhasha.mos.parse_mos_score`
- `bhasha.mos.aggregate_mos_ratings`
- `bhasha eval-mos` CLI command
- `mos_summary.json` evidence output
- `benchmark.csv` update with numeric MOS only when valid ratings exist

## Command

Fill the run's `mos_ratings_template.csv`, then run:

```bash
.venv\Scripts\python -m bhasha eval-mos --run-dir outputs\runs\<run_id>
```

Or use a separate ratings file:

```bash
.venv\Scripts\python -m bhasha eval-mos --run-dir outputs\runs\<run_id> --ratings path\to\human_ratings.csv
```

## CSV Format

```csv
sample_id,listener_id,score_1_to_5,same_speaker_ab,notes
en_xtts_001,rater_01,4.0,yes,Natural but slight accent
```

Blank scores are ignored. Scores outside 1-5 are reported in `mos_summary.json` as invalid rows. Bhasha does not fabricate MOS; samples without valid human ratings stay `pending_human_eval`.
