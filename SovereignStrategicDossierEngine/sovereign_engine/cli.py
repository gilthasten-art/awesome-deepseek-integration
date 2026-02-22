from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import SovereignStrategicDossierEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SovereignStrategicDossierEngine")
    parser.add_argument("--input", required=True, type=Path, help="Path to input JSON")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for generated artifacts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))

    engine = SovereignStrategicDossierEngine(output_dir=args.output_dir)
    try:
        result = engine.process(payload)
    finally:
        engine.close()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
