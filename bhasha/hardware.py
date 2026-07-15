from __future__ import annotations

import json
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass


@dataclass
class HardwareProfile:
    os: str
    python: str
    machine: str
    processor: str
    gpu_name: str | None
    gpu_driver_version: str | None
    cuda_version: str | None
    raw_nvidia_smi: str | None

    def to_dict(self) -> dict:
        return asdict(self)


def collect_hardware_profile() -> HardwareProfile:
    gpu_name = None
    driver_version = None
    cuda_version = None
    raw_nvidia_smi = None

    if shutil.which("nvidia-smi"):
        try:
            raw_nvidia_smi = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=name,driver_version",
                    "--format=csv,noheader",
                ],
                text=True,
                stderr=subprocess.STDOUT,
                timeout=5,
            ).strip()
            if raw_nvidia_smi:
                first = raw_nvidia_smi.splitlines()[0]
                parts = [part.strip() for part in first.split(",", maxsplit=1)]
                gpu_name = parts[0] if parts else None
                driver_version = parts[1] if len(parts) > 1 else None

            cuda_raw = subprocess.check_output(
                ["nvidia-smi"],
                text=True,
                stderr=subprocess.STDOUT,
                timeout=5,
            )
            cuda_version = _parse_cuda_version(cuda_raw)
        except Exception as exc:  # Hardware discovery must never fail a benchmark run.
            raw_nvidia_smi = json.dumps({"error": str(exc)})

    return HardwareProfile(
        os=f"{platform.system()} {platform.release()}",
        python=platform.python_version(),
        machine=platform.machine(),
        processor=platform.processor(),
        gpu_name=gpu_name,
        gpu_driver_version=driver_version,
        cuda_version=cuda_version,
        raw_nvidia_smi=raw_nvidia_smi,
    )


def _parse_cuda_version(nvidia_smi_output: str) -> str | None:
    marker = "CUDA Version:"
    if marker not in nvidia_smi_output:
        return None
    after = nvidia_smi_output.split(marker, maxsplit=1)[1].strip()
    return after.split()[0]
