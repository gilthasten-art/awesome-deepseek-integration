from __future__ import annotations

import json
from pathlib import Path

from sovereign_engine.engine import SovereignStrategicDossierEngine


def _payload() -> dict:
    return {
        "founder_profile": {"founder_name": "A", "company_name": "B", "experience_highlights": []},
        "business_strategy": {"sectors": ["Health"], "core_offerings": ["X"], "milestones": []},
        "loan_request": {"requested_amount": 100000, "term_months": 60, "use_of_proceeds": {}},
        "compliance": {"jurisdictions": ["US"], "standards": ["SOC2"], "policies": [], "controls": []},
        "financial_projections": [{"period": "2026-Q1", "revenue": 10, "cost": 5, "cashflow": 5}],
        "risk_inputs": {"market_risk": 20, "regulatory_risk": 30, "technology_risk": 40, "execution_risk": 50},
    }


def test_regenerate_on_change(tmp_path: Path) -> None:
    engine = SovereignStrategicDossierEngine(tmp_path)
    try:
        first = engine.process(_payload())
        assert json.loads(first["artifacts"])
        second = engine.process(_payload())
        assert second["changed"] == "False"

        changed_payload = _payload()
        changed_payload["financial_projections"][0]["revenue"] = 20
        third = engine.process(changed_payload)
        assert third["changed"] == "True"
    finally:
        engine.close()
