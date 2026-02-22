from __future__ import annotations

from .models import RiskReport


def build_risk_report(risk_inputs: dict, projection_summary: dict) -> RiskReport:
    market = float(risk_inputs.get("market_risk", 50))
    regulatory = float(risk_inputs.get("regulatory_risk", 50))
    technology = float(risk_inputs.get("technology_risk", 50))
    execution = float(risk_inputs.get("execution_risk", 50))

    overall = round((market + regulatory + technology + execution) / 4, 2)

    margin_factor = min(max(projection_summary.get("operating_margin_pct", 0) / 40, 0), 1)
    cashflow_factor = 1 if projection_summary.get("total_cashflow", 0) > 0 else 0.4
    risk_penalty = max(0, (100 - overall) / 100)

    readiness = round((margin_factor * 45 + cashflow_factor * 25 + risk_penalty * 30), 2)

    narrative = (
        f"Overall risk score is {overall}/100. Capital readiness is {readiness}/100 based on "
        f"financial resilience and risk posture."
    )
    return RiskReport(overall_risk_score=overall, capital_readiness_score=readiness, narrative=narrative)
