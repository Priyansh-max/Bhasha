from __future__ import annotations

import datetime as dt
import traceback
from pathlib import Path

from .adapters import get_adapter
from .hardware import collect_hardware_profile
from .reporting import write_audio_index, write_benchmark_csv, write_json, write_mos_template
from .schema import GenerationRequest, GenerationResult, LanguageConfig, ModelConfig, PromptConfig, SuiteConfig


def run_suite(
    suite: SuiteConfig,
    *,
    model_filter: str | None = None,
    language_filter: str | None = None,
    include_disabled: bool = False,
) -> Path:
    run_id = _new_run_id(suite.suite_id)
    run_dir = suite.output_root / run_id
    audio_dir = run_dir / "audio"
    run_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    hardware = collect_hardware_profile()
    languages = {language.id: language for language in suite.languages}

    rows: list[dict] = []
    failures: list[dict] = []

    selected_models = [
        model
        for model in suite.models
        if (include_disabled or model.enabled)
        and (model_filter is None or model.id == model_filter)
    ]

    selected_prompts = [
        prompt
        for prompt in suite.prompts
        if language_filter is None or prompt.language == language_filter
    ]

    for model in selected_models:
        for prompt in selected_prompts:
            language = languages.get(prompt.language)
            if language is None:
                rows.append(_row_for_failure(run_id, suite, model, None, prompt, "failed", "unknown", "Prompt language is not configured"))
                continue

            if prompt.language not in model.languages:
                rows.append(_row_for_failure(run_id, suite, model, language, prompt, "unsupported", "unsupported_language", "Model does not list this language"))
                continue

            for repeat_index in range(suite.repeat_count):
                sample_id = _sample_id(model, prompt, repeat_index)
                output_audio = audio_dir / prompt.language / model.id / f"{sample_id}.wav"
                request = GenerationRequest(
                    run_id=run_id,
                    sample_id=sample_id,
                    language=language,
                    model=model,
                    prompt=prompt,
                    output_audio=output_audio,
                )

                try:
                    adapter = get_adapter(model.adapter)
                    result = adapter.generate(request)
                except KeyError as exc:
                    result = GenerationResult(
                        status="skipped",
                        output_audio=None,
                        generation_time_seconds=None,
                        audio_duration_seconds=None,
                        latency_type="not_applicable",
                        failure_type="dependency_error",
                        failure_reason=str(exc),
                    )
                except Exception as exc:
                    result = GenerationResult(
                        status="failed",
                        output_audio=None,
                        generation_time_seconds=None,
                        audio_duration_seconds=None,
                        latency_type="batch_full_clip",
                        failure_type="model_error",
                        failure_reason=str(exc),
                    )
                    failures.append(
                        {
                            "sample_id": sample_id,
                            "model_id": model.id,
                            "prompt_id": prompt.id,
                            "traceback": traceback.format_exc(),
                        }
                    )

                row = _row_for_result(run_id, suite, language, model, prompt, request, result)
                rows.append(row)
                if result.status != "success":
                    failures.append(row)

    metadata = {
        "run_id": run_id,
        "suite": suite,
        "hardware_profile": hardware,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "notes": "MOS, ASR WER/CER, and speaker similarity are pending later milestones.",
    }

    write_benchmark_csv(run_dir / "benchmark.csv", rows)
    write_json(run_dir / "metadata.json", metadata)
    write_json(run_dir / "failures.json", failures)
    write_mos_template(run_dir / "mos_ratings_template.csv", rows)
    write_audio_index(run_dir / "audio_samples_index.md", rows)

    return run_dir


def _new_run_id(suite_id: str) -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{suite_id}"


def _sample_id(model: ModelConfig, prompt: PromptConfig, repeat_index: int) -> str:
    return f"{prompt.language}_{model.id}_{prompt.id}_r{repeat_index + 1:02d}"


def _row_for_result(
    run_id: str,
    suite: SuiteConfig,
    language: LanguageConfig,
    model: ModelConfig,
    prompt: PromptConfig,
    request: GenerationRequest,
    result: GenerationResult,
) -> dict:
    return {
        "run_id": run_id,
        "sample_id": request.sample_id,
        "suite_id": suite.suite_id,
        "language": language.id,
        "model_id": model.id,
        "prompt_id": prompt.id,
        "input_text": prompt.text,
        "reference_audio": str(request.reference_audio) if request.reference_audio else "",
        "output_audio": str(result.output_audio) if result.output_audio else "",
        "generation_time_seconds": _round(result.generation_time_seconds),
        "audio_duration_seconds": _round(result.audio_duration_seconds),
        "rtf": _round(result.rtf),
        "latency_type": result.latency_type,
        "time_to_first_audio_seconds": _round(result.time_to_first_audio_seconds),
        "asr_model": "pending",
        "asr_transcript": "",
        "wer": "pending",
        "cer": "pending",
        "speaker_embedding_model": "pending",
        "speaker_similarity": "not_applicable" if not model.supports_voice_cloning else "pending",
        "mos": "pending_human_eval",
        "status": result.status,
        "failure_type": result.failure_type or "",
        "failure_reason": result.failure_reason or "",
    }


def _row_for_failure(
    run_id: str,
    suite: SuiteConfig,
    model: ModelConfig,
    language: LanguageConfig | None,
    prompt: PromptConfig,
    status: str,
    failure_type: str,
    failure_reason: str,
) -> dict:
    language_id = language.id if language else prompt.language
    sample_id = f"{language_id}_{model.id}_{prompt.id}_failed"
    return {
        "run_id": run_id,
        "sample_id": sample_id,
        "suite_id": suite.suite_id,
        "language": language_id,
        "model_id": model.id,
        "prompt_id": prompt.id,
        "input_text": prompt.text,
        "reference_audio": "",
        "output_audio": "",
        "generation_time_seconds": "",
        "audio_duration_seconds": "",
        "rtf": "",
        "latency_type": "not_applicable",
        "time_to_first_audio_seconds": "",
        "asr_model": "pending",
        "asr_transcript": "",
        "wer": "pending",
        "cer": "pending",
        "speaker_embedding_model": "pending",
        "speaker_similarity": "pending" if model.supports_voice_cloning else "not_applicable",
        "mos": "pending_human_eval",
        "status": status,
        "failure_type": failure_type,
        "failure_reason": failure_reason,
    }


def _round(value: float | None) -> float | str:
    if value is None:
        return ""
    return round(value, 6)

