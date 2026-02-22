from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from regenerative_dossier_engine.models import BusinessIdentity, FounderIdentity


class IdentityJSONStore:
    """Persists founder and business identity records in JSON for portability."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.identity_file = self.base_path / "identity.json"

    def save(self, founder: FounderIdentity, business: BusinessIdentity) -> None:
        payload = {"founder": asdict(founder), "business": asdict(business)}
        self.identity_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> tuple[FounderIdentity, BusinessIdentity]:
        payload = json.loads(self.identity_file.read_text(encoding="utf-8"))
        founder = FounderIdentity(**payload["founder"])
        business = BusinessIdentity(**payload["business"])
        return founder, business
