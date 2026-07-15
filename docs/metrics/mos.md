# MOS Naturalness

MOS means Mean Opinion Score. It is a human listening score, usually from 1 to 5.

```text
1 = bad / unnatural
3 = acceptable
5 = excellent / human-like
```

## What It Measures

MOS captures perceived naturalness better than automatic metrics can. It must come from real listeners.

## Workflow

Bhasha creates a blank `mos_ratings_template.csv` for successful generated samples. Fill it with real listener ratings, then aggregate:

```bash
python -m bhasha eval-mos --run-dir outputs/runs/<run_id>
```

Or pass a separate ratings file:

```bash
python -m bhasha eval-mos --run-dir outputs/runs/<run_id> --ratings path/to/human_ratings.csv
```

## CSV Format

```csv
sample_id,listener_id,score_1_to_5,same_speaker_ab,notes
en_xtts_001,rater_01,4.0,yes,Natural but slight accent
```

## Outputs

- Updates `benchmark.csv`: `mos`.
- Writes `mos_summary.json` with rating counts, averages, standard deviation, notes, and invalid rows.

Blank scores are ignored. Invalid scores are reported. Bhasha leaves MOS as `pending_human_eval` until valid listener ratings exist.
