from __future__ import annotations

import json
from pathlib import Path

from sovereign_strategic_dossier_engine.cli import run_from_json


def test_generates_documents_and_detects_unchanged(tmp_path: Path) -> None:
    payload = {
        "founder": {
            "name": "Avery Stone",
            "background": "Regulated AI systems architect",
            "certifications": "CISSP",
            "governance_focus": "AI compliance-first deployment",
        },
        "sectors": [
            {
                "sector": "Healthcare",
                "innovation_thesis": "Audit-safe automation",
                "market_strategy": "Provider pilot",
                "expected_revenue": 1000000,
            }
        ],
        "projections": [
            {"year": 2026, "revenue": 1000000, "cogs": 250000, "opex": 450000, "debt_service": 120000},
            {"year": 2027, "revenue": 1400000, "cogs": 300000, "opex": 520000, "debt_service": 130000},
        ],
        "risks": [
            {
                "category": "Regulatory",
                "likelihood": "medium",
                "impact": "medium",
                "mitigation": "Quarterly control refresh",
            }
        ],
    }

    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps(payload))

    db_path = tmp_path / "test.db"
    output_dir = tmp_path / "out"

    manifest = run_from_json(str(payload_file), str(db_path), str(output_dir), force=False)
    assert "innovation_dissertation.pdf" in manifest["dissertation_pdf"]
    assert (output_dir / "innovation_dissertation.pdf").exists()
    assert (output_dir / "innovation_dissertation.docx").exists()
    assert (output_dir / "sba_loan_packet.pdf").exists()
    assert (output_dir / "compliance_governance.docx").exists()

    no_change = run_from_json(str(payload_file), str(db_path), str(output_dir), force=False)
    assert no_change["status"] == "no_changes"

    payload["projections"][1]["revenue"] = 1500000
    payload_file.write_text(json.dumps(payload))
    changed = run_from_json(str(payload_file), str(db_path), str(output_dir), force=False)
    assert "capital_readiness_score" in changed
