from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProjectionRow:
    period: str
    revenue: float
    cost: float
    cashflow: float


@dataclass(frozen=True)
class RiskReport:
    overall_risk_score: float
    capital_readiness_score: float
    narrative: str


def normalize_input(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize shape and ensure predictable defaults."""
    normalized = {
        "founder_profile": payload.get("founder_profile", {}),
        "business_strategy": payload.get("business_strategy", {}),
        "loan_request": payload.get("loan_request", {}),
        "compliance": payload.get("compliance", {}),
        "financial_projections": payload.get("financial_projections", []),
        "risk_inputs": payload.get("risk_inputs", {}),
    }
    return normalized
