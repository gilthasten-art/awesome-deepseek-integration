from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class IdentityStore:
    """Stores founder and business identity data in JSON files."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, identity_payload: dict[str, Any]) -> Path:
        target = self.base_path / "identity.json"
        with target.open("w", encoding="utf-8") as handle:
            json.dump(identity_payload, handle, indent=2, ensure_ascii=False)
        return target

    def load(self) -> dict[str, Any]:
        target = self.base_path / "identity.json"
        if not target.exists():
            return {}
        with target.open("r", encoding="utf-8") as handle:
            return json.load(handle)
