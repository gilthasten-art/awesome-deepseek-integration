from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import SovereignStrategicDossierEngine
from .models import FinancialProjection, FounderProfile, RiskItem, SectorInitiative


def _load_payload(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def run_from_json(payload_path: str, db_path: str, output_dir: str, force: bool) -> dict[str, str]:
    payload = _load_payload(payload_path)
    founder = FounderProfile(**payload["founder"])
    sectors = [SectorInitiative(**item) for item in payload["sectors"]]
    projections = [FinancialProjection(**item) for item in payload["projections"]]
    risks = [RiskItem(**item) for item in payload["risks"]]

    engine = SovereignStrategicDossierEngine(db_path=db_path, output_dir=output_dir)
    try:
        return engine.save_inputs(founder, sectors, projections, risks, force_regenerate=force)
    finally:
        engine.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Sovereign Strategic Dossier Engine")
    parser.add_argument("payload", help="Path to JSON payload with founder, sectors, projections, risks")
    parser.add_argument("--db", default="sovereign_dossier.db", help="SQLite database path")
    parser.add_argument("--output", default="generated_docs", help="Output directory for files")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if no data changed")
    args = parser.parse_args()

    manifest = run_from_json(args.payload, db_path=args.db, output_dir=args.output, force=args.force)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
