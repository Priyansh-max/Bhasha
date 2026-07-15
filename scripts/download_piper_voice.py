from __future__ import annotations

import urllib.request
from pathlib import Path

FILES = {
    "models/piper/en_US-lessac-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
    "models/piper/en_US-lessac-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json",
}


def main() -> None:
    for destination, url in FILES.items():
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            print(f"exists: {path}")
            continue
        print(f"download: {url}")
        urllib.request.urlretrieve(url, path)
        print(f"saved: {path}")


if __name__ == "__main__":
    main()
